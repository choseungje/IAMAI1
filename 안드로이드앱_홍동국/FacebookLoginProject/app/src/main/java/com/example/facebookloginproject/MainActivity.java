package com.example.facebookloginproject;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.facebook.CallbackManager;
import com.facebook.login.LoginManager;
import com.facebook.login.widget.LoginButton;

import java.util.Arrays;

//페이스북은 CallbackManager를 통해 콜백을 관리합니다.
// 로그인 요청 시에 결과는 onActivityResult() 메소드를 통해 들어오게 되는데,
// 로그인 결과를 CallbackManager로 넘겨주어 관리하도록 합니다.
// 한편, 로그인 버튼에 콜백을 등록하여 CallbackManager에 담겨진 로그인 결과를
// 저희가 생성한 LoginCallback으로 전달하여, 로그인 결과에 대한 처리를 할 수 있도록 합니다.
public class MainActivity extends AppCompatActivity {
    private Context mContext;

    private LoginButton btn_facebook_login;

    private LoginCallback mLoginCallback;
    private CallbackManager mCallbackManager;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mContext = getApplicationContext();

        mCallbackManager = CallbackManager.Factory.create();
        mLoginCallback = new LoginCallback();

        btn_facebook_login=(LoginButton) findViewById(R.id.btn_facebook_login);
        btn_facebook_login.setReadPermissions(Arrays.asList("public_profile", "email"));
        btn_facebook_login.registerCallback(mCallbackManager, mLoginCallback);




    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data){
        mCallbackManager.onActivityResult(requestCode, resultCode,data);
        super.onActivityResult(requestCode, resultCode,data);
    }



}
