package comm.protocol
{
	import comm.Conn;
	
	import flash.utils.Dictionary;

	public class ClientProtocol
	{
		private static var client_commands:Dictionary = new Dictionary();
		
		client_commands['chat.call_into'] = new Object();
		client_commands.handler = null_handler;
		client_commands.requires = new Array('chat_id', 'sender');
		
		client_commands['chat.broadcast'] = new Object();
		client_commands.handler = null_handler;
		client_commands.requires = new Array('chat_id', 'sender', 'msg');
		
		client_commands['game.call_into'] = new Object();
		client_commands.handler = null_handler;
		client_commands.requires = new Array('game_id', 'sender');
		
		client_commands['game.initialize'] = new Object();
		client_commands.handler = null_handler;
		client_commands.requires = new Array('game_id', 'chat_id', 'sender',
											 'black', 'white', 'size', 'komi', 'handicap',
											 'timed_game', 'main_time', 'byo_yomi',
											 'moves_handicap', 'moves_all', 'resigned', 'score');
		
		
		public static function process(conn:Conn, message:*):void {
			// TODO
			
			// final command execution should be done in main app, not in this lib
			// how?
		}
		
		private static function null_handler():void {
			trace("comm.protocol.ClientProtocol", "null_handler called");
		}
	}
}