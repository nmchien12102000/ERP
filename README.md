# Mini ERP – repo vỏ (submodule)

Repo này chỉ chứa phần lõi. Code 3 module nằm ở 3 repo private riêng, gắn vào đây bằng submodule:

| Thư mục | Repo | Ai được xem |
|---|---|---|
| `core/`, `tests/`, `main.py` | `erp` (repo này) | Tất cả |
| `modules/fi` | `erp-fi` | Dev FI + Leader |
| `modules/sd` | `erp-sd` | Dev SD + Leader |
| `modules/mm` | `erp-mm` | Dev MM + Leader |

Máy không có code của module nào thì module đó tự được thay bằng **bản giả** (`core/fakes`).

## Dev: chỉ tải module của mình

    git clone https://github.com/<owner>/erp.git
    cd erp
    git submodule update --init modules/sd

## Leader: tải đủ cả 3

    git clone --recurse-submodules https://github.com/<owner>/erp.git

## Chạy

    python main.py
    python -m unittest -v

## Quy tắc

1. Module KHÔNG import code của module khác. Gọi qua `core.services.get("mm")`.
2. Hợp đồng giữa các module nằm ở `core/contract_tests/`; bản giả ở `core/fakes/`. Chỉ Leader sửa.
3. Tên bảng database bắt đầu bằng mã module: `fi_`, `sd_`, `mm_`.
