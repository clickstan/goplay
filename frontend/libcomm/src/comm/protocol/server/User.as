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
	}
}