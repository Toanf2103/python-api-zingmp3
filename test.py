import asyncio

async def process_item(item):
    # Thực hiện xử lý bất đồng bộ trên từng phần tử item ở đây
    # Ví dụ: Đợi một khoảng thời gian ngẫu nhiên để mô phỏng xử lý bất đồng bộ
    import random
    import time
    await time.sleep(1)
    return f"Processed {item}"

original_list = range(100)  # Danh sách gồm 100 key ban đầu
processed_list = []

def add(x):
    processed_list.append(x)
# Sử dụng asyncio để xử lý bất đồng bộ cho từng phần tử
async def test():
    tasks = [process_item(item) for item in original_list]
    results = await asyncio.gather(*tasks)
    # results = await asyncio.gather(*tasks)
    processed_list.extend(results)
    
    # Kết quả được gom lại thành một mảng mới
    
test()
# asyncio.run(test())
print(processed_list)
