package com.example.apptest;

import com.facebook.FacebookCallback;
import com.facebook.Profile;
import com.facebook.login.LoginResult;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.JsonToken;
import android.util.Log;
import android.widget.Button;
import android.widget.Toast;

import androidx.core.app.ActivityCompat;

import com.facebook.AccessToken;
import com.facebook.FacebookException;
import com.facebook.GraphRequest;
import com.facebook.GraphResponse;

import org.json.JSONObject;

//Callback 클래스는 FacebookCallback<LoginResult>를 상속해서 만들었습니다.
//
//구성은 심플합니다. 로그인 성공 시에 호출되는 onSussess(),
// 로그인 웹뷰 화면의 닫기 버튼을 눌러 로그인을 취소하였을 때 호출되는 onCancel(),
// 기타 에러 상황으로 로그인에 실패하였을 경우 호출되는 onError().
// 여기서는 로그인에 성공하였을 경우, 사용자 정보를 요청하여 결과를 받도록 구성하였습니다.
//사용자 정보 요청에서는 Bundle로 원하는 필드 값들을 파라미터로 넘겨준 뒤, Json 형태로 결과를 받을 수 있습니다.


public class LoginCallback extends Activity implements FacebookCallback<LoginResult> {


    // 로그인 성공 시 호출 됩니다. Access Token 발급 성공.
    @Override
    public void onSuccess(LoginResult loginResult) {

        Log.e("Callback :: ", "onSuccess");


    }

    // 로그인 창을 닫을 경우, 호출됩니다.
    @Override
    public void onCancel() {
        Log.e("Callback :: ", "onCancel");
        //여기에 프로그램을 끄는 코드작성
        //ActivityCompat.finishAffinity(LoginCallback.this);
        //System.exit(0);


    }


    // 로그인 실패 시에 호출됩니다.
    @Override
    public void onError(FacebookException error) {
        Log.e("Callback :: ", "onError : " + error.getMessage());


    }


    // 로그인성공시 사용자 정보 요청함
    public void requestMe(AccessToken token) {

        GraphRequest graphRequest = GraphRequest.newMeRequest(token,
                new GraphRequest.GraphJSONObjectCallback() {
                    @Override
                    public void onCompleted(JSONObject object, GraphResponse response) {
                        Log.e("result",object.toString());

                    }
                });



        Bundle parameters = new Bundle();
        parameters.putString("fields", "id, name, email, gender, birthday");
        graphRequest.setParameters(parameters);
        graphRequest.executeAsync();


    }


}
