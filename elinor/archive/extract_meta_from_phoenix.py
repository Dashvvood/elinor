import os
import re
from pathlib import Path
import pandas as pd
from datetime import datetime

def extract_metadata_from_path(filepath):
    """从文件路径中提取元数据"""
    path = Path(filepath)
    
    # 直接从路径结构中确定Split
    split = 'Test' if 'test' in path.parts else 'Train'
    
    # 解析包含日期的文件夹名 (如: 01April_2010_Thursday_heute-6694)
    date_folder = path.parent.name
    folder_pattern = re.compile(r'(\d{2}[A-Za-z]+_\d{4}_\w+)_(tagesschau|heute)-(\d+)')
    folder_match = folder_pattern.match(date_folder)
    
    # 解析图片名 (如: images0001.png)
    file_match = re.search(r'images(\d{4})\.png', path.name)
    
    metadata = {
        'FilePath': str(path.relative_to(path.parents[2])),  # 相对于dataset目录的路径
        'Source': None,
        'FolderID': None,
        'FrameNumber': None,
        'Date': None,
        'Split': split
    } 
    
    if folder_match:
        # 提取日期部分 (如: 01April_2010_Thursday)
        date_part = folder_match.group(1)
        metadata['Source'] = folder_match.group(2)  # tagesschau或heute
        metadata['FolderID'] = folder_match.group(3)
        
        # 解析日期 (01April_2010 → 2010-04-01)
        try:
            day = date_part[:2]
            month = re.search(r'[A-Za-z]+', date_part).group()
            year = re.search(r'\d{4}', date_part).group()
            date_obj = datetime.strptime(f"{day} {month} {year}", "%d %B %Y")
            metadata['Date'] = date_obj.strftime("%Y-%m-%d")
        except Exception as e:
            print(f"日期解析错误: {date_part}, 错误: {e}")
    
    if file_match:
        metadata['FrameNumber'] = int(file_match.group(1))  # 0001 → 1
    
    return metadata

def collect_dataset_metadata(dataset_root):
    """收集数据集所有PNG文件的元数据"""
    metadata_list = []
    
    # 只遍历train和test目录
    for split_dir in ['train', 'test']:
        split_path = Path(dataset_root) / split_dir
        if not split_path.exists():
            continue
            
        # 遍历每个日期文件夹
        for date_folder in split_path.iterdir():
            if not date_folder.is_dir():
                continue
                
            # 获取所有PNG文件并按帧号排序
            png_files = sorted(
                [f for f in date_folder.glob('images*.png')],
                key=lambda x: int(re.search(r'images(\d+)\.png', x.name).group(1))
            )
            
            for file in png_files:
                metadata = extract_metadata_from_path(file)
                metadata_list.append(metadata)
    
    # 创建DataFrame并排序
    df = pd.DataFrame(metadata_list)
    df.sort_values(by=['Split', 'FolderID', 'FrameNumber'], inplace=True)
    return df[['FolderID', 'FrameNumber', 'Source', 'Date', 'Split', 'FilePath']]

def main():
    dataset_root = input("请输入dataset目录路径: ").strip()
    output_file = "dataset_metadata.csv"
    
    print("正在收集数据集元数据...")
    df = collect_dataset_metadata(dataset_root)
    
    print(f"找到 {len(df)} 个PNG文件 (Train: {len(df[df['Split']=='Train'])}, Test: {len(df[df['Split']=='Test'])})")
    df.to_csv(output_file, index=False)
    print(f"元数据已保存到 {output_file}")
    
    print("\n数据示例:")
    print(df.head())

if __name__ == "__main__":
    main()