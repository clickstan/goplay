package comm
{
	import comm.protocol.ClientProtocol;
	import comm.protocol.server.Util;
	
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	import flash.net.Socket;
	import flash.utils.Dictionary;
	import flash.utils.unescapeMultiByte;
	
	import mx.controls.Alert;
	import mx.utils.ObjectUtil;
	
	public class Conn
	{
		private var socket:Socket = new Socket();
		
		private var response_handlers:Dictionary = new Dictionary();	// {trans : [handler]}
		
		// user defined event handlers
		private var event_connect_handlers:Array = new Array();
		private var event_disconnect_handlers:Array = new Array();
		private var event_ioError_handlers:Array = new Array();
		private var event_securityError_handlers:Array = new Array();
		
		public function Conn()
		{
			socket.addEventListener(Event.CONNECT, event_connect);
			socket.addEventListener(Event.CLOSE, event_disconnect);
			socket.addEventListener(IOErrorEvent.IO_ERROR, event_ioError);
			socket.addEventListener(SecurityErrorEvent.SECURITY_ERROR, event_securityError);
			socket.addEventListener(ProgressEvent.SOCKET_DATA, event_socketData);
		}
		
		// -- event listeners
		
		private function event_connect(event:Event):void {
			trace("comm.Conn - event - Connect");
			
			for each (var handler:Function in event_connect_handlers)
				handler(event);
		}
		
		private function event_disconnect(event:Event):void {
			trace("comm.Conn - event - Close");
			
			for each (var handler:Function in event_disconnect_handlers)
				handler(event);
		}
		
		private function event_ioError(event:IOErrorEvent):void {
			trace("comm.Conn - event - IOError", event.text);
			
			for each (var handler:Function in event_ioError_handlers)
				handler(event);
		}
		
		private function event_securityError(event:SecurityErrorEvent):void {
			trace("comm.Conn - event - SecurityError", event.text);
			
			for each (var handler:Function in event_securityError_handlers)
				handler(event);
		}
		
		private function event_socketData(event:ProgressEvent):void {
			var object:Object = socket.readObject();
			trace("comm.Conn - event - SocketData", ObjectUtil.toString(object));
			
			var command:String = null;
			var trans:int = -1;
			
			if (object.hasOwnProperty("command"))
				command = object.command;
			
			if (object.hasOwnProperty("trans"))
				trans = object.trans;
			
			if (command != null)
				ClientProtocol.process(this, object);
			else if (trans >= 0)
				if (response_handlers.hasOwnProperty(trans)) {
					for each (var handler:Function in response_handlers[trans])
						handler(object);
					delete response_handlers[trans]
				}
		}
		
		// -- public methods
		
		public function connect(hostname:String, port:uint):void {
			socket.connect(hostname, port);
		}
		
		public function disconnect():void {
			socket.close();
		}
		
		public function send(object:*, trans:int=-1):void {
			if (trans >= 0)
				object.trans = trans;
			
			socket.writeObject(object);
			socket.flush();
		}
		
		/* addEventHandler
		 * This function is an abstraction of the addEventListener method for sockets,
		 * the event listeners defined in this class will call the added event handlers.
		 *
		 * Excluding ProgressEvent.SOCKET_DATA, all socket events are allowed.
		 */ 
		public function addEventHandler(eventType:String, handler:Function):void {
			switch (eventType) {
				case Event.CONNECT:
					event_connect_handlers.push(handler);
					break;
				case Event.CLOSE:
					event_disconnect_handlers.push(handler);
					break;
				case IOErrorEvent.IO_ERROR:
					event_ioError_handlers.push(handler);
					break;
				case SecurityErrorEvent.SECURITY_ERROR:
					event_securityError_handlers.push(handler);
					break;
				default:
					trace("event type not allowed: " + eventType, "comm.Client - addEventHandler"); 
			}
		}
		
		/* addResponseHandler
		 * This is the client-side equivalent for the server's addResponseCallback.
		 * 'handler' will be called when a message, that doesn't have a 'command' property,
		 * with the specified 'trans' number is intercepted.  Handler will receive message
		 * object as parameter.
		 * 
		 * Response handlers of a given 'trans' are removed after used.
		 */
		public function addResponseHandler(handler:Function, trans:int):void {
			if (response_handlers.hasOwnProperty(trans))
				response_handlers[trans].push(handler);
			else
				response_handlers[trans] = new Array(handler);
		}
	}
}