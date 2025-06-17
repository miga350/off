import os
import subprocess
import hashlib


def file_hash(path: str) -> str:
    """Calculate SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def verify_signature(path: str) -> dict:
    """Verify PDF signature using CryptoPro tools (if available)."""
    result = {
        'has_signature': False,
        'valid': False,
        'signer': None,
        'signing_time': None,
        'cert_info': None,
        'errors': []
    }
    try:
        proc = subprocess.run([
            'cryptcp',
            '-verify',
            path
        ], capture_output=True, text=True)
        output = proc.stdout + proc.stderr
        result['has_signature'] = 'Issuer' in output or 'Subject' in output
        result['valid'] = proc.returncode == 0
        result['cert_info'] = output.strip()
    except FileNotFoundError:
        result['errors'].append('CryptoPro not installed')
    except Exception as e:
        result['errors'].append(str(e))
    return result
