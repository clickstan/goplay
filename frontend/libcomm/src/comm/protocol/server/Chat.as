package comm.protocol.server
{
	import comm.protocol.server.Util;
	
	public class Chat
	{
		public static function broadcast(chat_id:int, msg:String):Object {
			return {'command'  : 'chat.broadcast',
				'chat_id' : chat_id,
				'msg'     : msg,
				'trans'   : Util.nextTrans()};
		}
	}
}