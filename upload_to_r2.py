import os
import boto3
from botocore.client import Config
from PIL import Image, ExifTags
import yaml
from datetime import datetime

# ================== 用户配置区域 ==================
R2_ACCESS_KEY = "76c491535e2dcb4ce2a19613fba3b2b7"                
R2_SECRET_KEY = "83ed71df4610b75787d6d3d5e1cece44d9f890af902201a0541490d5e2df7d29"            
R2_BUCKET = "my-photography"                     
R2_ENDPOINT = "https://b62862d0f5a13fad74b93ecfe3cf19fb.r2.cloudflarestorage.com"  
R2_PUBLIC_URL = "https://pub-867ab67c87ea4ab3988d1229f98eeb98.r2.dev"         

# 本地文件夹配置
LOCAL_IMAGE_DIR = "./photos_raw"      # 存放原始照片的文件夹
OUTPUT_WEBP_DIR = "./photos_webp"     # 临时存放转换后 WebP 的缓存文件夹
YAML_OUTPUT = "./data/photography.yml" # 生成的 Hugo 数据文件路径
# ==================================================

def convert_to_webp(input_path, output_path, quality=85):
    """将图片转换为 WebP 格式"""
    with Image.open(input_path) as im:
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            im.save(output_path, 'webp', quality=quality, lossless=True)
        else:
            im.save(output_path, 'webp', quality=quality)

def upload_to_r2(local_path, remote_key):
    """上传文件到 R2，设置公共读权限"""
    session = boto3.session.Session()
    client = session.client('s3',
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )
    client.upload_file(local_path, R2_BUCKET, remote_key, ExtraArgs={'ACL': 'public-read'})

def get_image_date(image_path):
    """提取拍摄日期"""
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if exif:
            for tag_id, value in exif.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                if tag_name == 'DateTimeOriginal':
                    date_str = value.split()[0].replace(':', '-')
                    return date_str
    except Exception as e:
        pass
    mtime = os.path.getmtime(image_path)
    return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

def main():
    os.makedirs(OUTPUT_WEBP_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(YAML_OUTPUT), exist_ok=True)

    if not os.path.exists(LOCAL_IMAGE_DIR):
        print(f"文件夹 {LOCAL_IMAGE_DIR} 不存在，正在创建...")
        os.makedirs(LOCAL_IMAGE_DIR)
        return

    local_files = []
    for season_folder in os.listdir(LOCAL_IMAGE_DIR):
        folder_path = os.path.join(LOCAL_IMAGE_DIR, season_folder)
        if os.path.isdir(folder_path):
            for f in os.listdir(folder_path):
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    local_files.append((season_folder, f))

    if not local_files:
        print(f"在 {LOCAL_IMAGE_DIR} 中没有找到图片。")
        return

    print(f"📸 扫描到 {len(local_files)} 张本地图片，开始同步生成纯净数据...")

    # 核心修改：抛弃旧数据，每次运行都创建一个全新的空列表！
    fresh_photos_data = [] 
    processed_upload = 0
    skipped_upload = 0

    for season_folder, filename in local_files:
        base = os.path.splitext(filename)[0]
        # 加上季节前缀，防止不同文件夹下有同名文件
        unique_title = f"{season_folder}_{base}" 
        
        input_path = os.path.join(LOCAL_IMAGE_DIR, season_folder, filename)
        webp_filename = unique_title + '.webp'
        webp_path = os.path.join(OUTPUT_WEBP_DIR, webp_filename)
        remote_key = f"photos/{season_folder}/{webp_filename}"
        r2_url = f"{R2_PUBLIC_URL}/{remote_key}"

        # 核心修改：利用本地 webp 文件夹做缓存判断，避免重复上传 R2
        if os.path.exists(webp_path):
            print(f" ⏩ 跳过上传 (已有缓存): {season_folder}/{filename}")
            skipped_upload += 1
        else:
            print(f" 🔄 处理新照片: {season_folder}/{filename}")
            try:
                convert_to_webp(input_path, webp_path, quality=85)
                print(f"    ⏫ 上传至 R2: {remote_key}")
                upload_to_r2(webp_path, remote_key)
                processed_upload += 1
            except Exception as e:
                print(f"    ❌ 处理失败: {e}")
                continue # 如果上传失败，就不加入 YAML

        # 核心修改：无论是否跳过上传，都将正确的最新信息写入我们全新的数据列表中
        date_taken = get_image_date(input_path)
        fresh_photos_data.append({
            'title': unique_title,
            'display_title': base,
            'url': r2_url,
            'date': date_taken,
            'season': season_folder
        })

    # 核心修改：排序后，使用 'w' 模式暴力覆写 YAML，彻底抹杀所有“幽灵旧数据”
    fresh_photos_data.sort(key=lambda x: x.get('date', '1970-01-01'), reverse=True)
    with open(YAML_OUTPUT, 'w', encoding='utf-8') as f:
        yaml.dump(fresh_photos_data, f, allow_unicode=True, sort_keys=False)

    print(f"\n🎉 完美重构结束！")
    print(f"-> 实际新上传: {processed_upload} 张")
    print(f"-> 跳过已上传: {skipped_upload} 张")
    print(f"-> 纯净的 YAML 数据清单已重新生成至 {YAML_OUTPUT}")

if __name__ == '__main__':
    main()