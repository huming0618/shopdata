var dwr = {};
var result = null;
var error = null;
var getResult = function(){
  return result;
}
var getError = function(){
  return error;
}

dwr.engine = {};

dwr.engine._remoteHandleCallback = function(parm1, parm2, jsonText){
  result = JSON.parse(jsonText);
}

dwr.engine._remoteHandleException = function(){
  error = Array.prototype.slice.call(arguments, 0);
}
