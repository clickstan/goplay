package comm.protocol
{
	import comm.Conn;
	
	import flash.utils.Dictionary;
	
	import mx.utils.ObjectUtil;
 
	public class ClientProtocol
	{
		private static var client_commands:Dictionary = new Dictionary();
		
		private static var last_command:String;
		
		// -- chat commands
		
		client_commands['chat.call_into'] = {'handler' : null_handler,
											 'requires' : new Array('chat_id', 'sender')};
		
		client_commands['chat.broadcast'] = {'handler' : null_handler,
											 'requires' : new Array('chat_id', 'sender', 'msg')};
		
		// -- game commands
		
		client_commands['game.call_into'] = {'handler' : null_handler,
											 'requires' : new Array('game_id', 'sender')};
		
		client_commands['game.initialize'] = {'handler' : null_handler,
											  'requires' : new Array('game_id', 'chat_id',
												  					 'black', 'white', 'size', 'komi', 'handicap',
												  					 'timed_game', 'main_time', 'byo_yomi',
												  					 'moves_handicap', 'moves_all', 'resigned', 'score')};

		client_commands['game.new_public_game_request'] = {'handler' : null_handler,
															'requires' : new Array('white_plyr_a','black_plyr_a','size_a','status_a','gameid_a')};
		
		
		
		client_commands['game.play'] = {'handler' : null_handler,
										'requires' : new Array('game_id', 'color', 'move')};
		
		client_commands['game.final_score'] = {'handler' : null_handler,
											   'requires' : new Array('game_id', 'score')};
		
		// -- room commands
		
		client_commands['room.created'] = {'handler' : null_handler,
										   'requires' : new Array('room')};
		
		client_commands['room.destroyed'] = {'handler' : null_handler,
											 'requires' : new Array('room')};
		
		client_commands['room.adduser'] = {'handler' : null_handler,
										   'requires' : new Array('room', 'user')};
		
		client_commands['room.removeuser'] = {'handler' : null_handler,
											  'requires' : new Array('room', 'user')};
		client_commands['room.remove_public_game_request'] = {'handler' : null_handler,
			'requires' : new Array('room', 'white_plyr','black_plyr','gameid')};
		// -- commands end
		
		public static function process(conn:Conn, msg:Object):void {
			var command:String = null;
			var trans:int = -1;
			
			if (msg.hasOwnProperty("command"))
				command = msg.command;
			
			if (msg.hasOwnProperty("trans"))
				trans = msg.trans;
			
			delete msg.command;
			
			if (trans >= 0)
				delete msg.trans;
			
			if (!client_commands.hasOwnProperty(command)) {
				trace("comm.protocol.ClientProtocol", "process(...)", "unknown command");
				return
			}
			
			var args:Array = new Array(conn, trans);
			
			for each (var requirement:String in client_commands[command].requires) {
				if (msg.hasOwnProperty(requirement)) {
					args.push(msg[requirement]);
				} else {
					trace("comm.protocol.ClientProtocol", "process(...)", "missing arg: " + requirement);
					return
				}
			}
			
			last_command = command;
			
			client_commands[command].handler.apply(NaN, args);
		}
		
		private static function null_handler(...args):void {
			trace("comm.protocol.ClientProtocol", "null_handler called", last_command, args);
		}
		
		public static function setCommandHandler(command:String, handler:Function):void {
			if (client_commands.hasOwnProperty(command))
				client_commands[command].handler = handler;
			else
				trace("comm.protocol.ClientProtocol", "setCommanHandler(...)", "unknown command", command);
		}
	}
}