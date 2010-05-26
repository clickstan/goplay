from twisted.internet import protocol


class EngineProcessProtocol(protocol.ProcessProtocol):
    
    def __init__(self, game):
        self.game = game
        self.gc = game._config
        
        self.response_callbacks = []    # [callback]
    
    def connectionMade(self):
        self.send("boardsize %s" % self.gc.size)
        self.send("komi %s" % self.gc.komi)
        self.send("clear_board")
        
    def outReceived(self, data):
        for message in data.split('\n'):
            if (message != '') and (len(self.response_callbacks) > 0):
                self.response_callbacks.pop(0)(message)
    
    def processEnded(self, status):
        pass
    
    # --- utilities
    
    def addResponseCallback(self, f):
        """response will be the only parameter passed to the callbacks
        
        unlike GoPlayProtocol.addResponseCallback, all callbacks will be called
        on first data received after the callbacks were registered
        """
        self.response_callbacks.append(f)
        
    def send(self, text):
        self.transport.write(text+'\n')
        
    # --- commands
    
    def stop(self):
        self.send('quit')
        
    def play(self, color, pos, callback):
        def process_response(msg):
            callback(msg == '= ')
            
        self.addResponseCallback(process_response)
        self.send("play {0} {1}".format(color, pos))
        
    def genmove(self, color):
        self.send("genmove {0}".format(color))
        
    def final_score(self, callback):
        def process_response(msg):
            callback(msg[2:])
            
        self.addResponseCallback(process_response)
        self.send("final_score")