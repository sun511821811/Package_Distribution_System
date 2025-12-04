import os
import asyncio
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


import shutil


class ProcessService:
    def __init__(self):
        # Try to find apk-secure in PATH first (for Docker/Global install)
        self.tool_path = shutil.which("apk-secure")

        # If not found, fallback to local venv path (for local dev)
        if not self.tool_path:
            self.tool_path = os.path.join(os.getcwd(), "venv/bin/apk-secure")

        logger.info(f"Using apk-secure at: {self.tool_path}")

    async def process_package(self, package_id: int, file_path: str) -> str:
        """
        Process the package using apk-secure tool.
        Returns the path to the processed file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")

        output_dir = os.path.join(os.getcwd(), "uploads", str(package_id), "processed")
        os.makedirs(output_dir, exist_ok=True)

        filename = os.path.basename(file_path)
        output_path = os.path.join(output_dir, f"{filename}")

        # Ensure tool exists
        if not os.path.exists(self.tool_path):
            raise FileNotFoundError(f"apk-secure tool not found at {self.tool_path}")

        cmd = [self.tool_path, "protect", "--apk", file_path, "--output", output_path]

        logger.info(f"Running command for package {package_id}: {' '.join(cmd)}")

        # Create a temporary working directory for the tool execution
        import uuid

        work_dir = os.path.join(os.getcwd(), "temp_execution", str(uuid.uuid4()))
        os.makedirs(work_dir, exist_ok=True)

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=work_dir,  # Execute tool in this directory
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode()
                logger.error(f"Process failed: {error_msg}")
                raise Exception(f"APK Processing failed: {error_msg}")

            logger.info(f"Process success: {stdout.decode()}")

            if not os.path.exists(output_path):
                raise Exception("Output file was not created by the tool")

            return output_path

        except Exception as e:
            logger.error(f"Error running apk-secure: {str(e)}")
            raise
        finally:
            # Cleanup working directory
            if os.path.exists(work_dir):
                try:
                    import shutil

                    shutil.rmtree(work_dir)
                except Exception as e:
                    logger.error(f"Failed to cleanup work dir {work_dir}: {e}")


process_service = ProcessService()
