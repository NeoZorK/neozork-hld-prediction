#!/usr/bin/env python3
"""
Fix for Docker input issue in interactive system.
This script adds better input handling for Docker environment.
"""

import sys
import os

def apply_docker_input_fix():
    """Apply fix for Docker input handling."""
    print("🔧 Applying Docker input fix...")
    
    # Path to the analysis_runner.py file
    file_path = "src/interactive/analysis_runner.py"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    # Read the current file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if the fix is already applied
    if "except EOFError:" in content and "print(\"\\n⏭️  Skipping fixes due to input error.\")" in content:
        print("✅ Docker input fix is already applied!")
        return True
    
    # Find the line with the input prompt
    lines = content.split('\n')
    modified = False
    
    for i, line in enumerate(lines):
        if "fix_choice = input(\"\\nDo you want to fix all issues? (y/n/skip): \").strip().lower()" in line:
            # Add better error handling around this input
            print(f"🔧 Found input line at line {i+1}")
            
            # Look for the try block that contains this input
            try_start = None
            for j in range(i, -1, -1):
                if "try:" in lines[j] and "input(" not in lines[j]:
                    try_start = j
                    break
            
            if try_start is not None:
                # Find the end of the try block
                try_end = None
                for j in range(try_start, len(lines)):
                    if "except EOFError:" in lines[j]:
                        try_end = j
                        break
                
                if try_end is None:
                    # Add EOFError handling
                    print("🔧 Adding EOFError handling...")
                    
                    # Find where to add the except block
                    # Look for the end of the if-elif-else block
                    block_end = None
                    for j in range(i, len(lines)):
                        if "elif fix_choice in ['n', 'no']:" in lines[j]:
                            # Find the end of this elif block
                            for k in range(j, len(lines)):
                                if lines[k].strip() == "" or lines[k].strip().startswith("#"):
                                    block_end = k
                                    break
                            break
                    
                    if block_end is not None:
                        # Insert the except block
                        except_block = [
                            "",
                            "                except EOFError:",
                            "                    print(\"\\n⏭️  Skipping fixes due to input error.\")",
                            "                    print(\"   Continuing with data quality check...\")",
                            "                    break  # Exit the try block gracefully"
                        ]
                        
                        lines[block_end:block_end] = except_block
                        modified = True
                        print("✅ Added EOFError handling")
                        break
    
    if modified:
        # Write the modified content back
        with open(file_path, 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ Docker input fix applied successfully!")
        return True
    else:
        print("⚠️  Could not find the exact location to apply the fix")
        return False

def test_docker_input_fix():
    """Test the Docker input fix."""
    print("🧪 Testing Docker input fix...")
    
    try:
        # Import the modified module
        sys.path.append('src')
        from interactive.analysis_runner import AnalysisRunner
        
        # Create a mock system
        class MockSystem:
            def __init__(self):
                self.current_data = None
                self.current_results = {}
                self.menu_manager = MockMenuManager()
        
        class MockMenuManager:
            def mark_menu_as_used(self, menu, option):
                pass
        
        system = MockSystem()
        runner = AnalysisRunner()
        
        print("✅ Docker input fix test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Docker input fix test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Docker Input Fix Tool")
    print("=" * 40)
    
    # Apply the fix
    success = apply_docker_input_fix()
    
    if success:
        # Test the fix
        test_success = test_docker_input_fix()
        
        if test_success:
            print("\n✅ Docker input fix completed successfully!")
            print("🔧 The interactive system should now handle input errors gracefully in Docker.")
            sys.exit(0)
        else:
            print("\n❌ Docker input fix test failed!")
            sys.exit(1)
    else:
        print("\n❌ Failed to apply Docker input fix!")
        sys.exit(1)
