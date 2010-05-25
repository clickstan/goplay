package comm.protocol.server
{
	import comm.protocol.server.Util;
	
	import flash.utils.ByteArray;
	
	import mx.utils.SHA256;
	
	public class User
	{
		public static function login(username:String, password:String):Object {
			var ba_password:ByteArray = new ByteArray();
			ba_password.writeUTFBytes(password);
			return {'command'  : 'user.login',
					'username' : username,
					'password' : SHA256.computeDigest(ba_password),
					'trans'    : Util.nextTrans()};
		}
		
		public static function logout():Object {
			return {'command'  : 'user.logout',
					'trans'    : Util.nextTrans()};
		}
		
		
		public static function register(username:String, password:String, fullname:String, role:String):Object {
			var ba_password:ByteArray = new ByteArray();
			ba_password.writeUTFBytes(password);
			return {'command'  : 'user.register',
				'username' : username,
				'password' : SHA256.computeDigest(ba_password),
				'fullname' : fullname,
				'role'     : role,
				'trans'    : Util.nextTrans()};
		}
		
		public static function start_chat(username:String):Object {
			return {'command'  : 'user.start_chat',
				'username' : username,
				'trans'    : Util.nextTrans()};
		}
		
		public static function start_game(username:String,color:String):Object {
			return {'command'  : 'user.start_game',
				'username' : username,
				'color'	   : color,
				'trans'    : Util.nextTrans()};
		}
		
		public static function watch_game(game_id:int):Object {
			return {'command'  : 'user.watch_game',
				'game_id'  : game_id,
				'trans'    : Util.nextTrans()};
		}
		
		public static function broadcast(chat_id:int, msg:String):Object {
			return {'command'  : 'user.broadcast',
				'chat_id' : chat_id,
				'msg'     : msg,
				'trans'   : Util.nextTrans()};
		}
		
		public static function play(game_id:int, move:String):Object {
			return {'command'  : 'user.play',
				'game_id' : game_id,
				'move'    : move,
				'trans'   : Util.nextTrans()};
		}
		
		public static function resign(game_id:int):Object {
			return {'command'  : 'user.resign',
				'game_id'  : game_id,
				'trans'    : Util.nextTrans()};
		}
		
	}
}