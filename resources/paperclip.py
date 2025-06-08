"""

What does this do?

It runs every n seconds and copys the current clipboard. If its new it adds to a history sqllite db with max_history length (5 by default)
You can then retieve the clipboard history but it has some functions to rewrite the current clipboard back to a previous clipboard.
Why? because aac software have limited programming functionality. by passing content back and forth in the clipboard we can do stuff!

This program needs to be run like so:
1. On first ever run use
        paperclip.py setup
2. Then run it continually with
        paperclip.py listen
3. Then use either rewrite or passnew for the specific functions. E.g
        paperclip.py passnew
        paperclip.py rewrite

        passnew will pass the difference between the current pasteboard and pasteboard -1 to the command (NB: RelayKeys).
        You can change what program - by default though this is RelayKeys win cli - which should be in the same directory

        Rewrite will change the current pasteboard to history-n

NB: you can up the history length and the time check in the code.


"""

import sqlite3
import subprocess
import time

import pyperclip
import typer

conn = sqlite3.connect("copyhistory.sqlite")
global max_history
max_history = 5
now_list = ""


def setup_db():
    conn = sqlite3.connect("copyhistory.sqlite")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE "history" ("copy_string"	TEXT, "id"	INTEGER UNIQUE);""")
    cur.execute('CREATE TABLE "last_id" ("ID"	INTEGER);')
    cur.execute("INSERT INTO last_id (ID) VALUES (1);")
    for x in range(1, max_history + 1):
        cur.execute(
            "INSERT INTO history (ID,copy_string) VALUES (" + str(x) + ", 'Empty' )"
        )

    conn.commit()
    conn.close()


def add_history(copyBuffer: str = ""):
    conn = sqlite3.connect("copyhistory.sqlite")
    # Get last id
    cur = conn.cursor()
    cur.execute("select ID from last_id")
    row = cur.fetchone()
    last_id = int(row[0]) + 1

    # Reset-
    if last_id == max_history:
        last_id = 1

    cur.execute(
        "UPDATE history set copy_string = :copyBuffer where ID = :histID",
        {"copyBuffer": copyBuffer, "histID": last_id},
    )
    cur.execute("UPDATE last_id set ID=:histID", {"histID": last_id})
    conn.commit()
    conn.close()


def get_history(history: int = 0):
    # Get last id
    cur = conn.cursor()
    cur.execute("select ID from last_id")
    row = cur.fetchone()
    last_id = int(row[0])

    # This is going to mess up byt cant figure out logic
    if last_id == 1 and history != 0:
        # End of list
        last_id = max_history - history
    else:
        last_id = last_id - history

    # Get string with that ID
    cur.execute("SELECT copy_string from history where ID = " + str(last_id))
    row = cur.fetchone()
    cur.close()
    return row[0]


def check():
    last_item = get_history()
    now_item = pyperclip.paste()

    if now_item != last_item:
        add_history(now_item)
        return True


app = typer.Typer()


@app.command()
def setup():
    """
    Never used this before? Run this FIRST. It will setup the db. NB: No checking that youve done this.
    """
    setup_db()


@app.command()
def listen():
    """
    Listen for every 1 second for the pasteboard. Store the current pasteboard (text only) and just keep a history for the last max_hostory times
    """
    while True:
        check()
        time.sleep(1)


@app.command()
def passnew(sendto: str = "relaykeys-cli-win.exe", history: int = 1):
    """
    Find diff between pasteboard now - and historic pasteboard and send to command line - with argument of the new string
    """
    oldString = get_history(history)
    newString = pyperclip.paste()
    splitat = len(oldString)
    diffString = newString[splitat:]
    cmd = [sendto, "type:" + diffString]
    subprocess.run(cmd, shell=True)


@app.command()
def rewrite(history: int = 1):
    """
    Return a copy buffer with something from history. Provide an int that is the history minus that number,
    """
    typer.echo("Changing pasteboard to history -" + str(history))
    copyString = get_history(history)
    pyperclip.copy(copyString)


if __name__ == "__main__":
    app()
    add_history(pyperclip.paste())
