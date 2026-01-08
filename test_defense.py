from core.deception import start_guard
import os

folder = "test_vault"
if not os.path.exists(folder):
    os.makedirs(folder)

start_guard(folder)