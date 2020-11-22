import sqlite3

#Create MakerOracle Database
connection = sqlite3.connect('MakerOracle.db')

#Create cursor object
c = connection.cursor()


#Create tables
#Oracles table
c.execute('''CREATE TABLE oracles (oracle text PRIMARY KEY)''')
#Transaction hash table
c.execute('''CREATE TABLE transactions(oracle text, block integer, hash text PRIMARY KEY, input text, fee real)''')
#Input values table
c.execute('''CREATE TABLE inputs(hash text, time integer, price real, zzz real)''')

#Preload oracles table
c.execute('''INSERT INTO oracles VALUES('0xf723251896454458D4A78F1026d0155f23E853B9')''')
c.execute('''INSERT INTO oracles VALUES('0x7b01F2e680EEB3C7AaC02eb3E47BB5EA9a555E12')''')
c.execute('''INSERT INTO oracles VALUES('0xE3774Af455602C5a0EACC1b0f93e3cE0f65236ce')''')
c.execute('''INSERT INTO oracles VALUES('0x137Fdd00E9a866631d8DAf1a2116fb8df1ed07A7')''')
c.execute('''INSERT INTO oracles VALUES('0xf63A899DAf5F486131600EA31cbDD55C186b2E8b')''')
c.execute('''INSERT INTO oracles VALUES('0xbE4A09d4661f631f7E13aA2d5719EFC476fb211c')''')
c.execute('''INSERT INTO oracles VALUES('0x5e5430b97B4797cbC7adbA329d7740fB31a09A11')''')
c.execute('''INSERT INTO oracles VALUES('0x4a87875774799E2d3f15733bDab511092057d222')''')
c.execute('''INSERT INTO oracles VALUES('0x222EDdF60e3Af681Dc4cF4290f95eFa78237BA4a')''')
c.execute('''INSERT INTO oracles VALUES('0x20eD77585Be1b2BFD6056C64AEBaD41341E35907')''')
c.execute('''INSERT INTO oracles VALUES('0xaB6f43607F6551cdf96b95B90b44a0b7445e8934')''')
c.execute('''INSERT INTO oracles VALUES('0x0D0Ca466b85Bae24Ad9680840DE07b094799b99F')''')
c.execute('''INSERT INTO oracles VALUES('0xda4CC8c36e6ABEf5D309E9FC3aE0209caBd078C0')''')
#oracles = ['0xf723251896454458D4A78F1026d0155f23E853B9', '0x7b01F2e680EEB3C7AaC02eb3E47BB5EA9a555E12']





#commit executions
connection.commit()


#close connection
connection.close()
