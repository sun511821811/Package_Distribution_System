from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `users` MODIFY COLUMN `is_active` BOOL NOT NULL COMMENT '是否激活' DEFAULT 1;
        ALTER TABLE `users` MODIFY COLUMN `updated_at` DATETIME(6) NOT NULL COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `users` MODIFY COLUMN `username` VARCHAR(50) NOT NULL COMMENT '用户名';
        ALTER TABLE `users` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `users` MODIFY COLUMN `role` VARCHAR(20) NOT NULL COMMENT '角色 (admin: 管理员, operator: 操作员)' DEFAULT 'operator';
        ALTER TABLE `users` MODIFY COLUMN `password_hash` VARCHAR(128) NOT NULL COMMENT '密码哈希';
        ALTER TABLE `packages` MODIFY COLUMN `status` VARCHAR(20) NOT NULL COMMENT '处理状态 (pending: 等待中, processing: 处理中, processed_success: 处理成功, processed_failed: 处理失败)' DEFAULT 'pending';
        ALTER TABLE `packages` MODIFY COLUMN `description` LONGTEXT COMMENT '包描述';
        ALTER TABLE `packages` MODIFY COLUMN `updated_at` DATETIME(6) NOT NULL COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `packages` MODIFY COLUMN `name` VARCHAR(100) NOT NULL COMMENT '包名称';
        ALTER TABLE `packages` MODIFY COLUMN `type` VARCHAR(20) NOT NULL COMMENT '包类型 (如: apk, ipa, zip)';
        ALTER TABLE `packages` MODIFY COLUMN `sha256` VARCHAR(64) COMMENT '文件 SHA256 哈希';
        ALTER TABLE `packages` MODIFY COLUMN `is_distributing` BOOL NOT NULL COMMENT '是否开启分发' DEFAULT 1;
        ALTER TABLE `packages` MODIFY COLUMN `download_url` VARCHAR(500) COMMENT '固定下载链接';
        ALTER TABLE `packages` MODIFY COLUMN `file_size` BIGINT COMMENT '文件大小 (字节)';
        ALTER TABLE `packages` MODIFY COLUMN `r2_processed_path` VARCHAR(500) COMMENT '处理后包 R2 存储路径';
        ALTER TABLE `packages` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `packages` MODIFY COLUMN `current_version` VARCHAR(50) NOT NULL COMMENT '当前版本号';
        ALTER TABLE `packages` MODIFY COLUMN `r2_original_path` VARCHAR(500) COMMENT '原包 R2 存储路径';
        ALTER TABLE `original_package_history` MODIFY COLUMN `sha256` VARCHAR(64) NOT NULL COMMENT '文件 SHA256 哈希';
        ALTER TABLE `original_package_history` MODIFY COLUMN `package_id` INT NOT NULL COMMENT '关联的包';
        ALTER TABLE `original_package_history` MODIFY COLUMN `file_size` BIGINT NOT NULL COMMENT '文件大小 (字节)';
        ALTER TABLE `original_package_history` MODIFY COLUMN `uploaded_by_id` INT COMMENT '上传者';
        ALTER TABLE `original_package_history` MODIFY COLUMN `file_name` VARCHAR(255) NOT NULL COMMENT '文件名';
        ALTER TABLE `original_package_history` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL COMMENT '上传时间' DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `original_package_history` MODIFY COLUMN `r2_path` VARCHAR(500) NOT NULL COMMENT 'R2 存储路径';
        ALTER TABLE `original_package_history` MODIFY COLUMN `version` VARCHAR(50) NOT NULL COMMENT '原包内部版本号';
        ALTER TABLE `process_tasks` MODIFY COLUMN `status` VARCHAR(20) NOT NULL COMMENT '任务状态 (pending, processing, success, failed)' DEFAULT 'pending';
        ALTER TABLE `process_tasks` MODIFY COLUMN `updated_at` DATETIME(6) NOT NULL COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `process_tasks` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `process_tasks` MODIFY COLUMN `package_id` INT NOT NULL COMMENT '关联的包';
        ALTER TABLE `process_tasks` MODIFY COLUMN `result_message` LONGTEXT COMMENT '处理结果/错误信息';
        ALTER TABLE `process_tasks` MODIFY COLUMN `task_id` VARCHAR(50) NOT NULL COMMENT 'Celery 任务 ID';
        ALTER TABLE `process_tasks` MODIFY COLUMN `original_package_history_id` INT COMMENT '关联的原包历史';
        ALTER TABLE `process_tasks` MODIFY COLUMN `retry_count` INT NOT NULL COMMENT '重试次数' DEFAULT 0;
        ALTER TABLE `operation_logs` MODIFY COLUMN `target_id` VARCHAR(50) COMMENT '操作对象ID';
        ALTER TABLE `operation_logs` MODIFY COLUMN `target_type` VARCHAR(50) NOT NULL COMMENT '操作对象类型 (如: package, user)';
        ALTER TABLE `operation_logs` MODIFY COLUMN `username` VARCHAR(50) COMMENT '用户名 (冗余存储)';
        ALTER TABLE `operation_logs` MODIFY COLUMN `details` LONGTEXT COMMENT '操作详情 (JSON)';
        ALTER TABLE `operation_logs` MODIFY COLUMN `action` VARCHAR(50) NOT NULL COMMENT '操作动作 (如: upload, replace)';
        ALTER TABLE `operation_logs` MODIFY COLUMN `user_id` INT COMMENT '操作用户';
        ALTER TABLE `operation_logs` MODIFY COLUMN `ip_address` VARCHAR(50) COMMENT 'IP 地址';
        ALTER TABLE `operation_logs` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL COMMENT '操作时间' DEFAULT CURRENT_TIMESTAMP(6);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `users` MODIFY COLUMN `is_active` BOOL NOT NULL DEFAULT 1;
        ALTER TABLE `users` MODIFY COLUMN `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `users` MODIFY COLUMN `username` VARCHAR(50) NOT NULL;
        ALTER TABLE `users` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `users` MODIFY COLUMN `role` VARCHAR(20) NOT NULL DEFAULT 'operator';
        ALTER TABLE `users` MODIFY COLUMN `password_hash` VARCHAR(128) NOT NULL;
        ALTER TABLE `packages` MODIFY COLUMN `status` VARCHAR(20) NOT NULL DEFAULT 'pending';
        ALTER TABLE `packages` MODIFY COLUMN `description` LONGTEXT;
        ALTER TABLE `packages` MODIFY COLUMN `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `packages` MODIFY COLUMN `name` VARCHAR(100) NOT NULL;
        ALTER TABLE `packages` MODIFY COLUMN `type` VARCHAR(20) NOT NULL;
        ALTER TABLE `packages` MODIFY COLUMN `sha256` VARCHAR(64);
        ALTER TABLE `packages` MODIFY COLUMN `is_distributing` BOOL NOT NULL DEFAULT 1;
        ALTER TABLE `packages` MODIFY COLUMN `download_url` VARCHAR(500);
        ALTER TABLE `packages` MODIFY COLUMN `file_size` BIGINT;
        ALTER TABLE `packages` MODIFY COLUMN `r2_processed_path` VARCHAR(500);
        ALTER TABLE `packages` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `packages` MODIFY COLUMN `current_version` VARCHAR(50) NOT NULL;
        ALTER TABLE `packages` MODIFY COLUMN `r2_original_path` VARCHAR(500);
        ALTER TABLE `process_tasks` MODIFY COLUMN `status` VARCHAR(20) NOT NULL DEFAULT 'pending';
        ALTER TABLE `process_tasks` MODIFY COLUMN `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `process_tasks` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `process_tasks` MODIFY COLUMN `package_id` INT NOT NULL;
        ALTER TABLE `process_tasks` MODIFY COLUMN `result_message` LONGTEXT;
        ALTER TABLE `process_tasks` MODIFY COLUMN `task_id` VARCHAR(50) NOT NULL;
        ALTER TABLE `process_tasks` MODIFY COLUMN `original_package_history_id` INT;
        ALTER TABLE `process_tasks` MODIFY COLUMN `retry_count` INT NOT NULL DEFAULT 0;
        ALTER TABLE `operation_logs` MODIFY COLUMN `target_id` VARCHAR(50);
        ALTER TABLE `operation_logs` MODIFY COLUMN `target_type` VARCHAR(50) NOT NULL;
        ALTER TABLE `operation_logs` MODIFY COLUMN `username` VARCHAR(50);
        ALTER TABLE `operation_logs` MODIFY COLUMN `details` LONGTEXT;
        ALTER TABLE `operation_logs` MODIFY COLUMN `action` VARCHAR(50) NOT NULL;
        ALTER TABLE `operation_logs` MODIFY COLUMN `user_id` INT;
        ALTER TABLE `operation_logs` MODIFY COLUMN `ip_address` VARCHAR(50);
        ALTER TABLE `operation_logs` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `original_package_history` MODIFY COLUMN `sha256` VARCHAR(64) NOT NULL;
        ALTER TABLE `original_package_history` MODIFY COLUMN `package_id` INT NOT NULL;
        ALTER TABLE `original_package_history` MODIFY COLUMN `file_size` BIGINT NOT NULL;
        ALTER TABLE `original_package_history` MODIFY COLUMN `uploaded_by_id` INT;
        ALTER TABLE `original_package_history` MODIFY COLUMN `file_name` VARCHAR(255) NOT NULL;
        ALTER TABLE `original_package_history` MODIFY COLUMN `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `original_package_history` MODIFY COLUMN `r2_path` VARCHAR(500) NOT NULL;
        ALTER TABLE `original_package_history` MODIFY COLUMN `version` VARCHAR(50) NOT NULL;"""


MODELS_STATE = (
    "eJztXFtzm8gS/iuUnpwqnV00YgDlTXacjc8mdipRztna9RY1wCBTRqDlEke7lf++0wOIuw"
    "y6WDjWiyzPTCP4umem++se/hksPJM6wU9fAuoPXgv/DFyyoOxLoX0oDMhymbVCQ0h0hw+M"
    "2AjeQvQg9IkRskaLOAFlTSYNDN9ehrbnwtDbSDEsnX1S02KfGKm3kYzGym2kqrIK1zA9g1"
    "3EdudsuBs5DmuKXPuviGqhN6fhHb/JP/5kzbZr0m80SP9d3muWTR2z8Ay2Cdfk7Vq4WvK2"
    "Kzd8ywfCr+ma4TnRws0GL1fhneeuR9tuCK1z6lKfhBQuH/oRPBrcXQJB+rTxnWZD4lvMyZ"
    "jUIpETZs9WxWeNydWbBjwMzwWc2Z0F/GHn8Iv/QSNJkdSxLKlsCL+rdYvyPX7UDIdYkKNx"
    "PRt85/0kJPEIDmmGIaiXf68geXFH/Hoo8zIlQNmtlwFN4Ts0orcRlkSzJaoL8k1zqDsP79"
    "i/WNwA4f+mny7eTT+dYfEVXNtjUyCeGNdJD+JdgHKG6pIEwYPnm9odCe66QFsR3A++aUMG"
    "cDaFH0MY64bMcFbFESBsMLQxFY1tcB4htQXQbFQj0ryvCLXvOZ2MNx3/dMAOvCVc0+M/UI"
    "FXnZiIfSIFCWfEXNjua4GhrROGtiKJMmCO2aRPrwG9smSYt5FkYSPufbWNMlAbo0fNRo8q"
    "Rm8HGtse7K816jj3GOrEbViZ83IltehM8FB6Wa8xJY3IMrIAWMTAly1DZJ/mWG+H8QZMz2"
    "9u3sNFFkHwl8MbrmYlcL98OL9kE4BjzgbZIc0v4hnShk8BC42EVajfsJ7QXtB6rIuSJbDN"
    "RPSn9MuTLzVopMPyYhGGObYY/hNsSS2tmz2ZeeM6q0SzGzQxu/pw+Xk2/fCxoI4309kl9C"
    "Deuiq1nsmlmbC+iPD/q9k7Af4Vfr+5vuS4ekE49/kvZuNmvw/gnkgUeprrPWjEzG10aWsK"
    "V0Hd0dLcUt1Fyb6pW5YtCRStiy9Y3fzmwcW17nMOGjToxLh/IMwXKPTkzcLxiMm0u2QDyZ"
    "wGNetucom3v36iDuHIV+0gCQVufHtuu8T5GF/tnR2w7WbVwiaSZ9qLSUhUJLC1IWYSqiji"
    "Tqtu1poZRQaX4813RYjvwWzIe2/+xLjkt/zM5d0RHTAyD3lNZlftWqBFuYW4zFbM5Lfhlx"
    "KsEisa1MScaddwU9iZt+k2kSdG3Fcam+CljkUMYFH2XRZl6xR/rlFiyPQl8uwadfYl4oyt"
    "C2JNNhUnlrhVJCS28b7ZqOZISKz43/k7reA6o98aDLMkthW8+1zqYnzlsQHz1mqL76b9//"
    "K3WWHrT1E8+zD97VVh+39/c/1LOjyH+sX7m/MS2ByfDtabju9BPM/xVQwFXG1F1YUz9nei"
    "otcCWd4PBXtJhsLf9rInQaUR+T51Q+0r9YNaw26GvEa0B+hbeAy7lQSrB5JgI1cQxPFjq+"
    "V2fmjuKghJGNV4Ss1AZxJPSKosqWsCTLUgT0QppU8UpEMcL4oj4SyRiRkWaQLaUMFToMgc"
    "CkvfM2gQJP35SxT6mb8dRAZ8Kw+T0UgE1U6s/GCL2A41y2PxZMycE9VEuCfzzPQeXAgntM"
    "h3uui+LHf87UMG9gDrE8KjCR02EYVNtgnzB2FbIS1jivI0azfPNk20CuYWswwtsP+uI8zs"
    "eaMnWRB73KE8dGSCVQWQtrhVI6DhDdHim4qOIfWDVNTWxmOPc4LQeKwgcSyrWFIUrIpr17"
    "PatckHPb/6BdzQgkKqZFpwRxCWO613a4mjW3uGvvD53ZTdlbArSS9LLQxdlhrtHLpKDD3S"
    "vIRb0JYk7JQPqZM9Ouh4PLFiP0r4hARu6AC4SFRY0qnF95W2PNbhlxmGYbYdbaGAqvDxNZ"
    "DfSiWRPiNt2IFm2nAbehQm/ku3XElZumcZE2yJIv9u5UmZU/bklD05ZU9O2ZP+ZE/usvzG"
    "EXIm+534I2UM6RIMe6KsSvFuuMfUSUiC+x1zJx9jJ2LGrvRDwHPI3EmDVdWkUprtrzmzkv"
    "OnuZCWmwmtMi1r77eYrsNjlW/2FjrlWzKscpjosFJjC/cmA7MFp9ovLjVniXgETN5EpGpf"
    "eVVO23RNehWEjo94gezZstoSYdyGvMS4mb2Evp5QaYeD98SlHQ/+XpNp21A4uxA3e8T4OR"
    "A0Pyo9kPfVXmy8WKUHUi+4k3NZFDr+xrFLiLMfL7OmLFFfdQO1Knj05NZ25Yj7QLTCaVQs"
    "torsW8+n9tz9la44wFfspohr1Pk21Uq852KtTQE5a/bJwzpoLM1Q9ujsgWnMCF9MP19M31"
    "wOmqx2D8Cmx+p6b6pt4azOzXpI2zBvT84m7TXzVGO7uSh0He/3mF7Kg1dXnlvEdkOJbjxQ"
    "W+uzFXtUqKuB06IYwVmnjB05sUfZlE7x6QtjBKqu3dQ3FD5mIoeKPloCesGWK38l5HEVWg"
    "N7KrrjU35D0V1+NtcU3eUL7IZCUkI3FOLyuJ4UwbGogj2otmB3VutgNRdRVyV7VSOhUHMM"
    "jOjE+BnCvtEEFlyIvLNDEjtn6A9SZu3T0F8xnCO3JhpvXL1LUk8Xn4l1ipiM4OyOqptQ1q"
    "4jwBsrbY8N7Dk4+1HJjVPtQwrXqfbhpai7kqZvyux2o2EeucrROZn9RmD7XmBPdOKJ/Hp2"
    "5NemkpAdUe7FqfKnIW3KWnhkIe1KoB204ih/sr2uzqh08n1DdVE6UkvP23d9b1j+qLuMKS"
    "jIMk/vEMtlqVNM+sIKHeUdYvtcH8ovEeMVF6OJws1wks9Yb0VU7J8ugvcldSvcyiSOXQNQ"
    "en8VgjIA+J6dQ46TDUPBp0uHGLQnmIfEZ8uL1vngd1GsZ+jrFlBBhjyqPxGe7FxDAaZrv/"
    "TQlYXOCR19valXQV+4aJOGxHZqyOhN75BYi/QKXFWnnIc2sHD238831y1N+KlZTnsJQb5P"
    "g04ZgKLUkXG/+giVXcoYkniKtNVLUfZvyT8q21l0kV8o/VXDdrJNqmPJUSZxdF5rl1d8HZ"
    "h0iZJyludXFXOI96YNy7UxmRH1KaafUt827gY10XzSM9wUx5NszGPxe4r9S47LmzE4nelp"
    "P2Hbo3j4EyUwNTqAmAx/ngAe5HV07BdDWpe2B0e8wevKREpAfnHZA/5h2kY4FBw7CP/sJ6"
    "wbUISn3hw4lGOEkoMEFziv26efcnv5/i/t8UGd"
)
