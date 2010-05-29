package comm.protocol.server
{
	public class Util
	{
		private static var trans:int = 0;
		
		public static function nextTrans():int {
			return trans++;
		}
	}
}