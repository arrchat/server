
this.msgpack||(function(globalScope){globalScope.msgpack={pack:msgpackpack,unpack:msgpackunpack};var _bin2num={},_num2bin={},_buf=[],_idx=0,_error=0,_isArray=Array.isArray||(function(mix){return Object.prototype.toString.call(mix)==="[object Array]";}),_isUint8Array=function(mix){return Object.prototype.toString.call(mix)==="[object Uint8Array]";},_toString=String.fromCharCode,_MAX_DEPTH=512;function msgpackpack(data,toString){_error=0;var byteArray=encode([],data,0);return _error?false:toString?byteArrayToByteString(byteArray):byteArray;}
function msgpackunpack(data){_buf=typeof data==="string"?toByteArray(data):data;_idx=-1;return decode();}
function encode(rv,mix,depth){var size,i,iz,c,pos,high,low,sign,exp,frac;if(mix==null){rv.push(0xc0);}else if(mix===false){rv.push(0xc2);}else if(mix===true){rv.push(0xc3);}else{switch(typeof mix){case"number":if(mix!==mix){rv.push(0xcb,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff);}else if(mix===Infinity){rv.push(0xcb,0x7f,0xf0,0x00,0x00,0x00,0x00,0x00,0x00);}else if(Math.floor(mix)===mix){if(mix<0){if(mix>=-32){rv.push(0xe0+mix+32);}else if(mix>-0x80){rv.push(0xd0,mix+0x100);}else if(mix>-0x8000){mix+=0x10000;rv.push(0xd1,mix>>8,mix&0xff);}else if(mix>-0x80000000){mix+=0x100000000;rv.push(0xd2,mix>>>24,(mix>>16)&0xff,(mix>>8)&0xff,mix&0xff);}else{high=Math.floor(mix/0x100000000);low=mix&0xffffffff;rv.push(0xd3,(high>>24)&0xff,(high>>16)&0xff,(high>>8)&0xff,high&0xff,(low>>24)&0xff,(low>>16)&0xff,(low>>8)&0xff,low&0xff);}}else{if(mix<0x80){rv.push(mix);}else if(mix<0x100){rv.push(0xcc,mix);}else if(mix<0x10000){rv.push(0xcd,mix>>8,mix&0xff);}else if(mix<0x100000000){rv.push(0xce,mix>>>24,(mix>>16)&0xff,(mix>>8)&0xff,mix&0xff);}else{high=Math.floor(mix/0x100000000);low=mix&0xffffffff;rv.push(0xcf,(high>>24)&0xff,(high>>16)&0xff,(high>>8)&0xff,high&0xff,(low>>24)&0xff,(low>>16)&0xff,(low>>8)&0xff,low&0xff);}}}else{sign=mix<0;sign&&(mix*=-1);exp=((Math.log(mix)/0.6931471805599453)+1023)|0;frac=mix*Math.pow(2,52+1023-exp);low=frac&0xffffffff;sign&&(exp|=0x800);high=((frac/0x100000000)&0xfffff)|(exp<<20);rv.push(0xcb,(high>>24)&0xff,(high>>16)&0xff,(high>>8)&0xff,high&0xff,(low>>24)&0xff,(low>>16)&0xff,(low>>8)&0xff,low&0xff);}
break;case"string":iz=mix.length;pos=rv.length;rv.push(0);for(i=0;i<iz;++i){c=mix.charCodeAt(i);if(c<0x80){rv.push(c&0x7f);}else if(c<0x0800){rv.push(((c>>>6)&0x1f)|0xc0,(c&0x3f)|0x80);}else if(c<0x10000){rv.push(((c>>>12)&0x0f)|0xe0,((c>>>6)&0x3f)|0x80,(c&0x3f)|0x80);}}
size=rv.length-pos-1;if(size<32){rv[pos]=0xa0+size;}else if(size<0x100){rv.splice(pos,1,0xd9,size);}else if(size<0x10000){rv.splice(pos,1,0xda,size>>8,size&0xff);}else if(size<0x100000000){rv.splice(pos,1,0xdb,size>>>24,(size>>16)&0xff,(size>>8)&0xff,size&0xff);}
break;default:if(_isUint8Array(mix)){size=mix.length;if(size<0x100){rv.push(0xc4,size);}else if(size<0x10000){rv.push(0xc5,size>>8,size&0xff);}else if(size<0x100000000){rv.push(0xc6,size>>>24,(size>>16)&0xff,(size>>8)&0xff,size&0xff);}
Array.prototype.push.apply(rv,mix);break;}
if(++depth>=_MAX_DEPTH){_error=1;return rv=[];}
if(_isArray(mix)){size=mix.length;if(size<16){rv.push(0x90+size);}else if(size<0x10000){rv.push(0xdc,size>>8,size&0xff);}else if(size<0x100000000){rv.push(0xdd,size>>>24,(size>>16)&0xff,(size>>8)&0xff,size&0xff);}
for(i=0;i<size;++i){encode(rv,mix[i],depth);}}else{pos=rv.length;rv.push(0);size=0;for(i in mix){++size;encode(rv,i,depth);encode(rv,mix[i],depth);}
if(size<16){rv[pos]=0x80+size;}else if(size<0x10000){rv.splice(pos,1,0xde,size>>8,size&0xff);}else if(size<0x100000000){rv.splice(pos,1,0xdf,size>>>24,(size>>16)&0xff,(size>>8)&0xff,size&0xff);}}}}
return rv;}
function decode(){var size,i,iz,c,num=0,sign,exp,frac,ary,hash,buf=_buf,type=buf[++_idx];if(type>=0xe0){return type-0x100;}
if(type<0xc0){if(type<0x80){return type;}
if(type<0x90){num=type-0x80;type=0x80;}else if(type<0xa0){num=type-0x90;type=0x90;}else{num=type-0xa0;type=0xa0;}}
switch(type){case 0xc0:return null;case 0xc2:return false;case 0xc3:return true;case 0xca:num=buf[++_idx]*0x1000000+(buf[++_idx]<<16)+
(buf[++_idx]<<8)+buf[++_idx];sign=num&0x80000000;exp=(num>>23)&0xff;frac=num&0x7fffff;if(!num||num===0x80000000){return 0;}
if(exp===0xff){return frac?NaN:Infinity;}
return(sign?-1:1)*(frac|0x800000)*Math.pow(2,exp-127-23);case 0xcb:num=buf[++_idx]*0x1000000+(buf[++_idx]<<16)+
(buf[++_idx]<<8)+buf[++_idx];sign=num&0x80000000;exp=(num>>20)&0x7ff;frac=num&0xfffff;if(!num||num===0x80000000){_idx+=4;return 0;}
if(exp===0x7ff){_idx+=4;return frac?NaN:Infinity;}
num=buf[++_idx]*0x1000000+(buf[++_idx]<<16)+
(buf[++_idx]<<8)+buf[++_idx];return(sign?-1:1)*((frac|0x100000)*Math.pow(2,exp-1023-20)
+num*Math.pow(2,exp-1023-52));case 0xcf:num=buf[++_idx]*0x1000000+(buf[++_idx]<<16)+
(buf[++_idx]<<8)+buf[++_idx];return num*0x100000000+
buf[++_idx]*0x1000000+(buf[++_idx]<<16)+
(buf[++_idx]<<8)+buf[++_idx];case 0xce:num+=buf[++_idx]*0x1000000+(buf[++_idx]<<16);case 0xcd:num+=buf[++_idx]<<8;case 0xcc:return num+buf[++_idx];case 0xd3:num=buf[++_idx];if(num&0x80){return((num^0xff)*0x100000000000000+
(buf[++_idx]^0xff)*0x1000000000000+
(buf[++_idx]^0xff)*0x10000000000+
(buf[++_idx]^0xff)*0x100000000+
(buf[++_idx]^0xff)*0x1000000+
(buf[++_idx]^0xff)*0x10000+
(buf[++_idx]^0xff)*0x100+
(buf[++_idx]^0xff)+1)*-1;}
return num*0x100000000000000+
buf[++_idx]*0x1000000000000+
buf[++_idx]*0x10000000000+
buf[++_idx]*0x100000000+
buf[++_idx]*0x1000000+
buf[++_idx]*0x10000+
buf[++_idx]*0x100+
buf[++_idx];case 0xd2:num=buf[++_idx]*0x1000000+(buf[++_idx]<<16)+
(buf[++_idx]<<8)+buf[++_idx];return num<0x80000000?num:num-0x100000000;case 0xd1:num=(buf[++_idx]<<8)+buf[++_idx];return num<0x8000?num:num-0x10000;case 0xd0:num=buf[++_idx];return num<0x80?num:num-0x100;case 0xdb:num+=buf[++_idx]*0x1000000+(buf[++_idx]<<16);case 0xda:num+=buf[++_idx]<<8;case 0xd9:num+=buf[++_idx];case 0xa0:for(ary=[],i=_idx,iz=i+num;i<iz;){c=buf[++i];ary.push(c<0x80?c:c<0xe0?((c&0x1f)<<6|(buf[++i]&0x3f)):((c&0x0f)<<12|(buf[++i]&0x3f)<<6|(buf[++i]&0x3f)));}
_idx=i;return ary.length<10240?_toString.apply(null,ary):byteArrayToByteString(ary);case 0xc6:num+=buf[++_idx]*0x1000000+(buf[++_idx]<<16);case 0xc5:num+=buf[++_idx]<<8;case 0xc4:num+=buf[++_idx];var end=++_idx+num
var ret=buf.slice(_idx,end);_idx+=num;return ret;case 0xdf:num+=buf[++_idx]*0x1000000+(buf[++_idx]<<16);case 0xde:num+=(buf[++_idx]<<8)+buf[++_idx];case 0x80:hash={};while(num--){size=buf[++_idx]-0xa0;for(ary=[],i=_idx,iz=i+size;i<iz;){c=buf[++i];ary.push(c<0x80?c:c<0xe0?((c&0x1f)<<6|(buf[++i]&0x3f)):((c&0x0f)<<12|(buf[++i]&0x3f)<<6|(buf[++i]&0x3f)));}
_idx=i;hash[_toString.apply(null,ary)]=decode();}
return hash;case 0xdd:num+=buf[++_idx]*0x1000000+(buf[++_idx]<<16);case 0xdc:num+=(buf[++_idx]<<8)+buf[++_idx];case 0x90:ary=[];while(num--){ary.push(decode());}
return ary;}
return;}
function byteArrayToByteString(byteArray){try{return _toString.apply(this,byteArray);}catch(err){;}
var rv=[],i=0,iz=byteArray.length,num2bin=_num2bin;for(;i<iz;++i){rv[i]=num2bin[byteArray[i]];}
return rv.join("");}
function toByteArray(data){var rv=[],bin2num=_bin2num,remain,ary=data.split(""),i=-1,iz;iz=ary.length;remain=iz%8;while(remain--){++i;rv[i]=bin2num[ary[i]];}
remain=iz>>3;while(remain--){rv.push(bin2num[ary[++i]],bin2num[ary[++i]],bin2num[ary[++i]],bin2num[ary[++i]],bin2num[ary[++i]],bin2num[ary[++i]],bin2num[ary[++i]],bin2num[ary[++i]]);}
return rv;}
(function(){var i=0,v;for(;i<0x100;++i){v=_toString(i);_bin2num[v]=i;_num2bin[i]=v;}
for(i=0x80;i<0x100;++i){_bin2num[_toString(0xf700+i)]=i;}})();})(this);