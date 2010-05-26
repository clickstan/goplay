// ActionScript file
package comm.protocol.server {
	import comm.protocol.server.Util;
	
	import flash.utils.ByteArray;
	
	public class Room	{
	
		public static function get_all_rooms():Object {
			return {'command' : 'room.get_all_rooms',
				'trans'	  : Util.nextTrans()};
		}
		
		
		public static function getUsersFromRoom(name:String):Object {
			return {'command' : 'room.getUsersFromRoom',
				'name'		: name,
				'trans'	  : Util.nextTrans()};
		}
	}
}