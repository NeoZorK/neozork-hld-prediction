"""
Test module for checking mql5_feed folder paths in Docker container.
This test helps diagnose where mql5_feed folder is located in the container.
"""
import os
import pytest
from pathlib import Path


class TestContainerMQL5FeedPaths:
    """Test class for discovering mql5_feed folder paths in container."""
    
    def test_list_possible_paths(self):
        """List all possible paths where mql5_feed might be located."""
        possible_paths = [
            Path("/app/mql5_feed"),
            Path("/workspace/mql5_feed"),
            Path("/home/neozork/mql5_feed"),
            Path.cwd() / "mql5_feed",
            Path("/mql5_feed"),
            Path("/app"),
            Path("/workspace"),
            Path("/home/neozork"),
            Path.cwd(),
        ]
        
        print(f"\nCurrent working directory: {Path.cwd()}")
        print(f"Current user: {os.getenv('USER', 'unknown')}")
        print(f"Current user home: {os.path.expanduser('~')}")
        
        print("\nChecking possible mql5_feed locations:")
        found_paths = []
        
        for path in possible_paths:
            exists = path.exists()
            is_dir = path.is_dir() if exists else False
            print(f"  {path}: exists={exists}, is_dir={is_dir}")
            
            if exists and is_dir:
                found_paths.append(path)
                
                # List contents if it's a directory
                try:
                    contents = list(path.iterdir())
                    print(f"    Contents: {[item.name for item in contents]}")
                    
                    # Check if mql5_feed is inside this directory
                    mql5_feed_subdir = path / "mql5_feed"
                    if mql5_feed_subdir.exists():
                        print(f"    Found mql5_feed subdirectory at: {mql5_feed_subdir}")
                        found_paths.append(mql5_feed_subdir)
                        
                except PermissionError:
                    print(f"    Permission denied accessing {path}")
                except Exception as e:
                    print(f"    Error accessing {path}: {e}")
        
        print(f"\nFound {len(found_paths)} accessible directories")
        
        # Check if we found mql5_feed
        mql5_feed_found = any("mql5_feed" in str(path) for path in found_paths)
        assert mql5_feed_found, f"mql5_feed folder not found in any of the checked locations. Found paths: {found_paths}"
    
    def test_docker_volume_mounts(self):
        """Test if Docker volume mounts are working correctly."""
        # Check common Docker mount points
        mount_points = [
            Path("/app"),
            Path("/workspace"),
            Path("/data"),
            Path("/home/neozork"),
        ]
        
        print("\nChecking Docker mount points:")
        for mount_point in mount_points:
            if mount_point.exists():
                print(f"  {mount_point}: exists")
                try:
                    contents = list(mount_point.iterdir())
                    print(f"    Contents: {[item.name for item in contents[:10]]}")  # Show first 10 items
                except Exception as e:
                    print(f"    Error listing contents: {e}")
            else:
                print(f"  {mount_point}: does not exist")
    
    def test_environment_variables(self):
        """Test environment variables that might indicate container setup."""
        env_vars = [
            "DOCKER_CONTAINER",
            "PYTHONPATH",
            "PWD",
            "HOME",
            "USER",
            "PATH",
        ]
        
        print("\nEnvironment variables:")
        for var in env_vars:
            value = os.getenv(var, "not set")
            print(f"  {var}: {value}")
    
    def test_file_system_access(self):
        """Test basic file system access in container."""
        test_paths = [
            Path("/"),
            Path("/app"),
            Path("/tmp"),
            Path.cwd(),
        ]
        
        print("\nFile system access test:")
        for path in test_paths:
            if path.exists():
                print(f"  {path}: accessible")
                try:
                    # Try to create a test file
                    test_file = path / "test_access.tmp"
                    test_file.write_text("test")
                    test_file.unlink()  # Clean up
                    print(f"    Write access: OK")
                except Exception as e:
                    print(f"    Write access: FAILED - {e}")
            else:
                print(f"  {path}: not accessible")


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v", "-s"])  # -s to show print statements 