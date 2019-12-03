from passlib.hash import pbkdf2_sha256 as sha256
import pymysql.cursors
import redis

rdb = redis.Redis(host='localhost',port=6379,db=0)
db = pymysql.connect(host='localhost',
    user='tdtest',
    password='tdtest',
    db='tesdaq',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)


class UserModel():
    @classmethod
    def reset_password(cls, username, newpass):
        # ONLY call this with hashed new passwords.

        query = "UPDATE users SET Password='{}', Hashed=true WHERE Username='{}'".format(newpass,username)
        with db.cursor() as cursor:
            cursor.execute(query)
            db.commit()

    @classmethod
    def find_by_username(cls, username):
        query = "SELECT Username, Password, Hashed FROM users WHERE Username='{}'".format(username)

        with db.cursor() as cursor:
            cursor.execute(query)
            user =  cursor.fetchone()
            return user

    @staticmethod
    def generate_hash(password):
        # Generates password hash to store in DB.
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        # Checks submitted password against hashed DB string.
        return sha256.verify(password, hash)

class RevokedTokenModel():
    @staticmethod
    def add(token):
        rdb.rpush("blacklisted-tokens",token) 

    @staticmethod
    def check_blacklisted(token):
        l = rdb.lrange("blacklisted-tokens",0,-1)
        return(str.encode(token) in  l)
