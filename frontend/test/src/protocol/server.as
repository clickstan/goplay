// ActionScript file

import flash.utils.ByteArray;
import flash.utils.Dictionary;

import mx.utils.SHA256;


private var trans:uint = 0;

public function nextTrans():uint {
	return trans++;
}



public function login(username:String, password:String):Object {
	var ba_password:ByteArray = new ByteArray();
	ba_password.writeUTFBytes(password);
	return {'command'  : 'user.login',
			'username' : username,
			'password' : SHA256.computeDigest(ba_password),
			'trans'    : nextTrans()};
}