var express = require('express');
var fs = require('fs');
//배열코드
var arrcode =[];
var result = null;
var showresult = "";
//
var app = express(); //app을 리턴한다
var bodyParser = require('body-parser'); //post방식
app.locals.pretty = true; // jade를 이용한 html 이쁘게하기
app.set('view engine', 'jade'); //익스프레스와 제이드 연결?
app.set('views', './views') // 제이드 사용할 폴더
//url치고오는것 = get방식으로 오는것
//req는 응답 관련 함수들
//app.get == 라우터

app.use(express.static('public'));//정적인 파일이 위치한 디렉토리 경로설정
app.use(bodyParser.urlencoded({ limit:"50mb", extended: false})); //use에 바디파서를 붙인다 모든 정보는 바디파서 모듈을 거친다

app.get('/', function(req, res){
  res.send('Welcome to Home!'); //이 값을 응답할것이다
});


//

async function rTfFunc(){
    const tf = require("@tensorflow/tfjs-node")
    const model = await tf.loadLayersModel('file://C:/Users/gpaj1/myapp/test/tensorflowSave/model/tfjs_target_dir/model.json')
    const res = model.predict(tf.tensor4d(arrcode,[1,128,128,1])).arraySync();
    var max = 0;
    for(var i = 0; i < 8; i++){
	if(res[0][i] > max){
	  max = res[0][i];
	  result = i;
	}
    }
    switch(result){
	case 0:
		showresult="당신은 남성\n강아지를 닮으셨네요!";
		break;
	case 1:
		showresult="당신은 여성\n강아지를 닮으셨네요!";
		break;
	case 2:
		showresult="당신은 남성\n고양이를 닮으셨네요!";
		break;
	case 3:
		showresult="당신은 여성\n고양이를 닮으셨네요!";
		break;
	case 4:
		showresult="당신은 남성\n여우를 닮으셨네요!";
		break;
	case 5:
		showresult="당신은 여성\n여우를 닮으셨네요!";
		break;
	case 6:
		showresult="당신은 남성\n공룡을 닮으셨네요!";
		break;
	case 7:
		showresult="당신은 여성\n공룡을 닮으셨네요!";
		break;
	default: break;
    }//switch-End

}

//

app.post('/form', async function(req,res){
  var image = req.body.image;
  //배열처리코드
  var toarr = image.replace(/(\s*)/g, "");
  var toarr = toarr.replace(/\n/g, "");
  var toarr = toarr.replace("[", "");
  var toarr = toarr.replace("]", "");
  var toarr = toarr.replace(/;/g, ",");

  var colonarr = toarr.split(",");
  var codearr = colonarr.map(Number);
  for(var i = 0 ; i < codearr.length ; i++){
    arrcode.push(codearr[i]/255);
  }
  //배열처리코드End
  await rTfFunc();
  res.send(showresult);
  //다시처리가능하게 초기화
  arrcode =[];
  result = null;
  showresult = "";
  //초기화코드End

});

//

function base64_decode(base64str, file) {
    var bitmap = new Buffer(base64str, "base64");
    fs.writeFileSync(file, bitmap);
    console.log('******** base64로 인코딩되었던 파일 쓰기 성공 ********');
}

//

app.listen(3000, function(){
  console.log('Connected 3000 port!');
});
