import time, hashlib, asyncore, socket
from struct import *

import wx

def IPToInt( ip ):
       return int(socket.inet_aton(ip).encode('hex'),16)
    

class Package:
    def __init__( self, id ):
        self.id = id

    def SetClient( self, clientId ):
        self.client = clientId

    def SetTarget( self, host, port ):
        self.host = IPToInt( host )
        self.port = port

    def SetData( self, dataLength, data ):
        self.dataLen = dataLength
        self.data    = data

    def Generate( self ):
        return pack( 'IIHHs', self.id, self.host, self.port, self.dataLen, self.data )



class Client( asyncore.dispatcher ):
    def __init__( self, host, port ):
        asyncore.dispatcher.__init__( self )
        self.create_socket( socket.AF_INET, socket.SOCK_STREAM )
        
        self.host = host
        self.port = port

        self.buffer = ''

    def Connect( self ):
        self.connect( (self.host, self.port) )

    def handle_connect( self ):
        pass

    def handle_close( self ):
        self.close()

    def handle_read( self ):
        print( self.recv( 65500 ) )

    def writable( self ):
        time.sleep( 1 )
        return True

    def handle_write( self ):
        if( len( self.buffer ) > 0 ):
               sent = self.send( self.buffer )
               self.buffer = self.buffer[sent:]
        else:
               self.send( 'LIST:\r\n' )

    def JoinPool( self, pool ):
        self.send( 'REG:'+pool+'\r\n' )

    def NewPool( self ):
        self.send( 'NEWPOOL:\r\n' )


#m = hashlib.sha1()
#m.update( "".encode('utf-8') )
#print( m.hexdigest() )

#m = Package( 1 )
#m.SetTarget( '127.0.0.1', 80 )
#m.SetData( 5, "A\r\n\r\n" )
#print( m.Generate() )

class GUI( wx.Frame ):
	def __init__( self, *args, **kwargs ):
		super( GUI, self ).__init__( *args, **kwargs )
		self.InitUI()
		
	def InitUI( self ):
		menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		fileMenu.Append( wx.ID_NEW, '&New' )
		menubar.Append( fileMenu, '&File' )
		self.SetMenuBar( menubar )
		
		self.Bind( wx.EVT_IDLE, self.Idle )
		
		self.SetSize( (400, 400) )
		self.SetTitle( 'Pool Manager' )
		self.Centre()
		self.Show( True )
		
	def Idle( self, e ):
		asyncore.loop( count=1 )




def main():
	client = Client( 'localhost', 40000 )
	client.Connect()
	client.NewPool()
	
	manager = wx.App()
	gui     = GUI( None )
	manager.MainLoop()

if __name__ == '__main__':
	main()

