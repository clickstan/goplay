// ActionScript file

package comm.protocol.server
{
	import comm.protocol.server.Util;
	
	public class Game
	{

		public static function play(game_id:int, move:String):Object {
			return {'command'  : 'chat.play',
				'game_id' : game_id,
				'move'    : move,
				'trans'   : Util.nextTrans()};
		}
		
		public static function resign(game_id:int):Object {
			return {'command'  : 'chat.resign',
				'game_id'  : game_id,
				'trans'    : Util.nextTrans()};
		}
	}
}