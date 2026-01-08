from core.key_manager import create_shared_keys, recover_key

print("--- TESTING SHAMIR SPLIT ---")

print("Splitting keys...")
file_part, pass_part = create_shared_keys()

print(f"Part 1 (Simulated USB File): {file_part}")
print(f"Part 2 (User Password):      {pass_part}")

print("\nAttempting to recover...")
restored_key = recover_key(file_part, pass_part)

if restored_key:
    print(f"Success! Restored Key: {restored_key}")
else:
    print("Failed to restore key.")