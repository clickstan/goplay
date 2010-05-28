// ActionScript file
package comm.protocol.server {
	import comm.protocol.server.Util;
	
	import flash.utils.ByteArray;
	
	public class Room	{
	
		public static function get_all_rooms():Object {
			return {'command' : 'room.get_all_rooms',
				'trans'	  : Util.nextTrans()};
		}
		public static function get_public_games_list(room:String):Object {
			return {'command' : 'room.get_public_games_list',
					'room':room,
					'trans'    : Util.nextTrans()}
		}
		public static function request_public_game(room:String, color:String, size:int):Object {
			return {'command'  : 'room.request_public_game',
				'color'	   : color,
				'size'	   : size,
				'room'	   : room,
				'trans'    : Util.nextTrans()};
		}
		
		public static function getUsersFromRoom(name:String):Object {
			return {'command' : 'room.getUsersFromRoom',
				'name'		: name,
				'trans'	  : Util.nextTrans()};
		}
		
		public static function createRoom(name:String):Object {
			return {'command' : 'room.createRoom',
				'name'		: name,
				'trans'	  : Util.nextTrans()};
		}

		public static function openRoom(name:String):Object {
			return {'command' : 'room.openRoom',
				'name'		: name,
				'trans'	  : Util.nextTrans()};
		}
		
		public static function getChatId(roomName:String):Object{
			return {'command' : 'room.getChatId',
				'roomName'		: roomName,
				'trans'	  : Util.nextTrans()};
		}
	}
}