#!/usr/bin/env python3
"""
Codespace Control V3 - Auto-Deployed Terminal Bridge
This script is automatically deployed and started by V3
"""

import asyncio
import websockets
import subprocess
import json
import os
import sys
import signal
import pty
import select
import termios
import struct
import fcntl
from threading import Thread
import logging
import uuid
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TerminalSession:
    def __init__(self, session_id, websocket):
        self.session_id = session_id
        self.websocket = websocket
        self.master_fd = None
        self.slave_fd = None
        self.process = None
        self.running = True
        self.output_thread = None

    async def start_terminal(self):
        try:
            self.master_fd, self.slave_fd = pty.openpty()

            winsize = struct.pack('HHHH', 24, 80, 0, 0)
            fcntl.ioctl(self.slave_fd, termios.TIOCSWINSZ, winsize)

            env = os.environ.copy()
            env['TERM'] = 'xterm-256color'
            env['PS1'] = '\[\033[01;32m\]codespace@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]$ '

            self.process = subprocess.Popen(
                ['/bin/bash', '--login'],
                stdin=self.slave_fd,
                stdout=self.slave_fd,
                stderr=self.slave_fd,
                preexec_fn=os.setsid,
                env=env,
                cwd=os.path.expanduser('~')
            )

            self.output_thread = Thread(target=self._monitor_output, daemon=True)
            self.output_thread.start()

            await self.send_message({
                'type': 'terminal_ready',
                'session_id': self.session_id,
                'message': f'🚀 V3 Auto-Bridge Terminal Ready! Session: {self.session_id}'
            })

            logger.info(f"V3 Terminal session {self.session_id} started")
            return True

        except Exception as e:
            logger.error(f"Failed to start terminal: {e}")
            await self.send_message({
                'type': 'error',
                'message': f'Failed to start terminal: {str(e)}'
            })
            return False

    def _monitor_output(self):
        while self.running and self.master_fd:
            try:
                ready, _, _ = select.select([self.master_fd], [], [], 0.1)

                if ready:
                    data = os.read(self.master_fd, 4096)
                    if data:
                        output_message = {
                            'type': 'terminal_output',
                            'session_id': self.session_id,
                            'data': data.decode('utf-8', errors='ignore')
                        }

                        asyncio.create_task(self.send_message(output_message))

            except OSError:
                break
            except Exception as e:
                logger.error(f"Output monitoring error: {e}")
                break

    async def send_input(self, data):
        if self.master_fd and self.running:
            try:
                os.write(self.master_fd, data.encode('utf-8'))
            except Exception as e:
                logger.error(f"Failed to send input: {e}")

    async def resize_terminal(self, rows, cols):
        if self.master_fd:
            try:
                winsize = struct.pack('HHHH', rows, cols, 0, 0)
                fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, winsize)
                logger.info(f"Terminal resized to {rows}x{cols}")
            except Exception as e:
                logger.error(f"Failed to resize terminal: {e}")

    async def send_message(self, message):
        if self.websocket and not self.websocket.closed:
            try:
                await self.websocket.send(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to send WebSocket message: {e}")

    def cleanup(self):
        self.running = False

        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

        if self.master_fd:
            os.close(self.master_fd)
        if self.slave_fd:
            os.close(self.slave_fd)

        logger.info(f"V3 Terminal session {self.session_id} cleaned up")

class V3TerminalBridgeServer:
    def __init__(self, host='0.0.0.0', port=8765):
        self.host = host
        self.port = port
        self.sessions = {}
        self.running = True

    async def handle_client(self, websocket, path):
        session_id = str(uuid.uuid4())
        client_addr = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"V3 Bridge: New client connected: {client_addr} -> {session_id}")

        session = TerminalSession(session_id, websocket)
        self.sessions[session_id] = session

        try:
            if await session.start_terminal():
                async for raw_message in websocket:
                    try:
                        message = json.loads(raw_message)
                        await self.handle_message(session, message)
                    except json.JSONDecodeError:
                        await session.send_message({
                            'type': 'error',
                            'message': 'Invalid JSON message'
                        })
                    except Exception as e:
                        logger.error(f"Message handling error: {e}")

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"V3 Bridge: Client disconnected: {client_addr}")
        except Exception as e:
            logger.error(f"V3 Bridge: Client handling error: {e}")
        finally:
            session.cleanup()
            if session_id in self.sessions:
                del self.sessions[session_id]

    async def handle_message(self, session, message):
        msg_type = message.get('type')

        if msg_type == 'terminal_input':
            data = message.get('data', '')
            await session.send_input(data)

        elif msg_type == 'terminal_resize':
            rows = message.get('rows', 24)
            cols = message.get('cols', 80)
            await session.resize_terminal(rows, cols)

        elif msg_type == 'ping':
            await session.send_message({
                'type': 'pong',
                'timestamp': time.time(),
                'bridge_version': 'V3_AUTO_DEPLOYED'
            })

        else:
            await session.send_message({
                'type': 'error',
                'message': f'Unknown message type: {msg_type}'
            })

    def signal_handler(self, signum, frame):
        logger.info("V3 Bridge shutting down...")
        self.running = False

        for session in list(self.sessions.values()):
            session.cleanup()

        sys.exit(0)

    async def start_server(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        logger.info(f"🚀 V3 Auto-Deployed Bridge starting on {self.host}:{self.port}")

        try:
            server = await websockets.serve(
                self.handle_client,
                self.host,
                self.port,
                ping_interval=30,
                ping_timeout=10
            )

            logger.info(f"✅ V3 Bridge running on ws://{self.host}:{self.port}")
            logger.info(f"🔗 Ready for V3 Codespace Control connections")

            await server.wait_closed()

        except Exception as e:
            logger.error(f"V3 Bridge server error: {e}")
            raise

def main():
    import argparse

    parser = argparse.ArgumentParser(description='V3 Auto-Deployed Terminal Bridge')
    parser.add_argument('--host', default='0.0.0.0', help='Server host (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8765, help='WebSocket port (default: 8765)')

    args = parser.parse_args()

    server = V3TerminalBridgeServer(host=args.host, port=args.port)

    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        logger.info("V3 Bridge stopped by user")
    except Exception as e:
        logger.error(f"V3 Bridge error: {e}")

if __name__ == '__main__':
    main()
