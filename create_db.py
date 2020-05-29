import sqlite3
conn = sqlite3.connect("blog.db")

#	conn.execute("DROP TABLE users")
#	conn.commit()
#	conn.execute("DROP TABLE roles")
#	conn.commit()
#conn.execute("CREATE TABLE users(username text, role text, hash text, email_addr text, desc text, creation_date text, last_login text)")
#conn.commit()
#conn.execute("INSERT INTO users VALUES('admin','admin', 'cLzRnzbEwehP6ZzTREh3A4MXJyNo+TV8Hs4//EEbPbiDoo+dmNg22f2RJC282aSwgyWv/O6s3h42qrA6iHx8yfw=','hey', 'hey', 'hey', 'hey')")
#conn.execute("INSERT INTO admins VALUES('{}', '{}')".format("admin", "1d2382b2cf082f140136ee8b0eb46a8c"))
#conn.commit()


conn.execute("CREATE TABLE roles(role text, level int)")
conn.execute("INSERT INTO roles VALUES ('admin', 100)")
conn.commit()
