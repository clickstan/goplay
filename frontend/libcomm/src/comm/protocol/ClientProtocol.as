package comm.protocol
{
	import comm.Conn;
	
	import flash.utils.Dictionary;

	public class ClientProtocol
	{
		private static var client_commands:Dictionary = new Dictionary();
		
		private static var last_command:String;
		
		// -- chat commands
		
		client_commands['chat.call_into'] = new Object();
		client_commands.handler = null_handler;
		client_commands.requires = new Array('chat_id', 'sender');
		
		client_commands['chat.broadcast'] = new Object();
		client_commands.handler = null_handler;
		client_commands.requires = new Array('chat_id', 'sender', 'msg');
		
		// -- game commands
		
		client_commands['game.call_into'] = new Object();
		client_commands.handler = null_handler;
		client_commands.requires = new Array('game_id', 'sender');
		
		client_commands['game.initialize'] = new Object();
		client_commands.handler = null_handler;
		client_commands.requires = new Array('game_id', 'chat_id', 'sender',
											 'black', 'white', 'size', 'komi', 'handicap',
											 'timed_game', 'main_time', 'byo_yomi',
											 'moves_handicap', 'moves_all', 'resigned', 'score');
		
		client_commands['game.play'] = new Object();
		client_commands.handler = null_handler;
		client_commands.requires = new Array('game_id', 'color', 'move');
		
		client_commands['game.final_score'] = new Object();
		client_commands.handler = null_handler;
		client_commands.requires = new Array('game_id', 'score');
		
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
			
			var args:Array = new Array();
			
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
			trace("comm.protocol.ClientProtocol", "null_handler called", last_command, args.toString());
		}
		
		public static function setCommandHandler(command:String, handler:Function):void {
			if (client_commands.hasOwnProperty(command))
				client_commands[command].handler = handler;
			else
				trace("comm.protocol.ClientProtocol", "setCommanHandler(...)", "unknown command");
		}
	}
}