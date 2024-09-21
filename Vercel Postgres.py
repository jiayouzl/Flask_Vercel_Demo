# -*- coding: UTF-8 -*-

# 这是一个基于vercel的Postgres服务使用的Python3客户端DEMO
# 在vercel的环境变量中设置数据库连接信息(推荐)

# 登录 https://vercel.com/jiayouzls-projects/~/stores 点击 Create Database 选 Postgres 创建数据库
# 在 Postgres 控制面板中找到连接信息在Quickstart中可以找到
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import errors
from psycopg2.extras import RealDictCursor

# 从环境变量获取数据库连接信息
load_dotenv()  # 从.env文件中加载环境变量(本地测试时使用)
DATABASE_URL = os.environ.get("VERCEL_POSTGRES_DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require", connect_timeout=5)


def create_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100) UNIQUE
                )
            """
            )
        conn.commit()


def create_user(name, email):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id", (name, email))
                user_id = cur.fetchone()[0]
            conn.commit()
        print(f"用户创建成功，ID: {user_id}")
        return user_id
    except errors.UniqueViolation as e:
        print(f"创建用户时出错: {e}")
        print("该电子邮件的用户已存在。")
    except Exception as e:
        print(f"创建用户时发生错误: {e}")
    return None


def get_user(user_id):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user = cur.fetchone()
                if user:
                    print(f"检索到用户: {user}")
                else:
                    print(f"未找到ID为的用户: {user_id}")
                return user
    except Exception as e:
        print(f"在检索用户 {user_id} 时发生错误: {e}")
        return None


def update_user(user_id, name, email):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
            conn.commit()
        print(f"用户 {user_id} 更新成功。")
    except errors.UniqueViolation as e:
        print(f"更新用户 {user_id} 时出错: {e}")
        print("电子邮件地址已被使用。")
    except Exception as e:
        print(f"更新用户 {user_id} 时发生错误: {e}")


def delete_user(user_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
                if cur.rowcount > 0:
                    print(f"用户 {user_id} 已成功删除。")
                else:
                    print(f"未找到ID为的用户: {user_id}")
            conn.commit()
    except Exception as e:
        print(f"删除用户 {user_id} 时发生错误: {e}")


def clear_database(table_name=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if table_name:
                    # 清空指定的表
                    cur.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE")
                    print(f"表格'{table_name}'已清空。")
                else:
                    # 获取所有表名
                    cur.execute(
                        """
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'
                    """
                    )
                    tables = cur.fetchall()
                    # 清空所有表
                    for table in tables:
                        cur.execute(f"TRUNCATE TABLE {table[0]} RESTART IDENTITY CASCADE")
                    print("数据库中的所有表已被清空。")
            conn.commit()
    except Exception as e:
        print(f"清除数据库时发生错误： {e}")


def drop_tables(table_name=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if table_name:
                    # 删除指定的表
                    cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
                    print(f"表格 '{table_name}' 已被删除。")
                else:
                    # 获取所有表名
                    cur.execute(
                        """
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'
                    """
                    )
                    tables = cur.fetchall()
                    # 删除所有表
                    for table in tables:
                        cur.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE")
                    print("数据库中的所有表都已删除。")
            conn.commit()
    except Exception as e:
        print(f"删除表时发生错误: {e}")


def main():
    create_table()

    # 创建用户
    user_id = create_user("John Doe", "john@example.com")
    print(f"Created user with ID: {user_id}")

    # 获取用户
    user = get_user(user_id)
    print(f"Retrieved user: {user}")

    # 更新用户
    update_user(user_id, "John Smith", "john.smith@example.com")
    updated_user = get_user(user_id)
    print(f"Updated user: {updated_user}")

    # 删除用户
    # delete_user(user_id)
    # deleted_user = get_user(user_id)
    # print(f"Deleted user (should be None): {deleted_user}")


if __name__ == "__main__":
    main()

    # 清空特定表
    # clear_database("users")
    # 清空整个数据库
    # clear_database()

    # 删除 users 表
    # drop_tables("users")

    # 删除所有表
    # drop_tables()
