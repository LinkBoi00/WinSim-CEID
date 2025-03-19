import os
import sys
import argparse

def apply_patch(file_path, offset, original_bytes, new_bytes, common_bytes):
    """
    Applies a patch to the file by replacing the bytes at the specified offset and shows only the changed bytes.
   
    :param file_path: Path to the binary file (e.g., 'WinSim-stock.exe')
    :param offset: The offset where the modification will be made
    :param original_bytes: The original byte sequence to be replaced (for checking)
    :param new_bytes: The new byte sequence to insert at the offset
    :param common_bytes: The byte sequence that is common and should not be displayed
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False
        
    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        # Read the entire file into memory
        file_data = file.read()
   
    # Extract the original bytes at the specified offset
    current_bytes = file_data[offset:offset+len(original_bytes)]
   
    # Identify the part that will be replaced (exclude common bytes)
    diff_original = original_bytes[len(common_bytes):]
    diff_new = new_bytes[len(common_bytes):]
   
    # Print the original bytes vs. patched bytes (excluding common bytes)
    print(f"Original bytes at offset {hex(offset)} (excluding common part):")
    print(" ".join(f"{b:02X}" for b in diff_original))
   
    print(f"Patched bytes to be applied at offset {hex(offset)} (excluding common part):")
    print(" ".join(f"{b:02X}" for b in diff_new))
   
    # Apply the patch if the current bytes match the original bytes
    if current_bytes == original_bytes:
        # Create the modified file data
        modified_data = file_data[:offset] + new_bytes + file_data[offset+len(original_bytes):]
       
        # Save the modified content back to a new file
        with open(file_path, 'wb') as file:
            file.write(modified_data)
       
        print(f"Patch applied successfully to {file_path}")
        return True
    else:
        print(f"Warning: The original bytes at offset {hex(offset)} do not match the expected bytes.")
        print(f"Expected: {original_bytes.hex(' ')}")
        print(f"Found: {current_bytes.hex(' ')}")
        return False

def main(file_path='WinSim.exe'):
    # Define the patch details
    offset = 0x00006250  # Offset where the modification will be made
    common_bytes = bytes([0xC7, 0x05, 0x58, 0xAB, 0x47, 0x00, 0x01, 0x00, 0x00])
    original_bytes = bytes([0xE8, 0x03, 0xE0, 0x02, 0x00, 0xEB, 0x0A]) + common_bytes
    new_bytes = bytes([0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90]) + common_bytes
    
    # Apply the patch
    return apply_patch(file_path, offset, original_bytes, new_bytes, common_bytes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apply a binary patch to a file.')
    parser.add_argument('--file', '-f', default='WinSim.exe', 
                        help='Path to the file to be patched (default: WinSim.exe)')
    
    args = parser.parse_args()
    
    try:
        result = main(args.file)
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)