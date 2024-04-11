from bank import SavingsAccount, Bank
from socket import *
from codecs import decode

BUFSIZE = 1024
CODE = "ascii"

def main(fileName = "bank.dat"):
    """Creates the bank with the optional file name,
    wraps the window around it, and opens the window.
    Saves the bank when the window closes."""
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = 'localhost'
    bank = ATMClient(host, 50000)
    atm = ATM(bank)
    atm.mainloop()

    def login(self):
        """Attempts to login the customer.  If successful,
        enables the buttons, including logout."""
        name = self.nameField.getText()
        pin = self.pinField.getText()
        self.account = self.bank.get(name, pin)
        if self.account:
            self.statusField.setText("Hello, " + name + "!")
            self.balanceButton["state"] = "normal"
            self.depositButton["state"] = "normal"
            self.withdrawButton["state"] = "normal"
            self.loginButton["text"] = "logout"
            self.loginButton["command"] = self.logout
        else:
            self.statusField.setText("Name and pin not found!")

    def deposit(self):
        """Attempts a deposit. If not successful, displays
        error message in statusfield; otherwise, announces
        success."""
        amount = self.amountField.getNumber()
        message = self.account.deposit(amount)
        if message:
            self.statusField.setText(message)
        else:
            self.statusField.setText("Deposit successful!")
        
    def withdraw(self):
        """Attempts a withdrawal. If not successful, displays
        error message in statusfield; otherwise, announces
        success."""
        amount = self.amountField.getNumber()
        message = self.account.withdraw(amount)
        if message:
            self.statusField.setText(message)
        else:
            self.statusField.setText("Withdrawal successful!")

def main(fileName = "bank.dat"):
    """Creates the bank with the optional file name,
    wraps the window around it, and opens the window.
    Saves the bank when the window closes."""
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = 'localhost'
    bank = ATMClient(host, 50000)
    atm = ATM(bank)
    atm.mainloop()

class ATMClient(object):
    """Represents the client for a bank ATM.  Behaves like a Bank with the
    get method and an account with the getBalance, deposit, and withdraw
    methods."""

    def __init__(self, host, port):
        """Initialize the client."""
        address = (host, port)
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.connect(address)                         
        message = decode(self.server.recv(BUFSIZE), CODE)

    def get(self, name, pin):
        """Returns the client's account if it exists, or None if not."""
        self.server.send(bytes(name + "\n" + pin, CODE))
        message = decode(self.server.recv(BUFSIZE), CODE)
        if message == "success":
            return self
        else:
            return None

    def getBalance(self):
        """Returns the balance of the account."""
        self.server.send(bytes("balance\n" + "nada", CODE))
        message = decode(self.server.recv(BUFSIZE), CODE)
        return float(message)                        

    def deposit(self, amount):
        """Deposits amount and returns None if successful,
        or an error message if not."""
        self.server.send(bytes("deposit\n" + str(amount), CODE))
        message = decode(self.server.recv(BUFSIZE), CODE)
        if message == "success": return None
        else: return message

    def withdraw(self, amount):
        """Withdraws amount and returns None if successful,
        or an error message if not."""
        self.server.send(bytes("withdraw\n" + str(amount), CODE))
        message = decode(self.server.recv(BUFSIZE), CODE)
        if message == "success": return None
        else: return message

if __name__ == "__main__":
    main()
