package com.example.apptest;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.Signature;
import android.os.Bundle;
import android.os.Handler;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.toolbox.Volley;
import com.facebook.CallbackManager;
import com.facebook.login.LoginManager;
import com.facebook.login.widget.LoginButton;

import org.json.JSONException;
import org.json.JSONObject;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;

public class LoginActivity extends AppCompatActivity {

    private EditText et_id, et_pass;
    private Button btn_login, btn_register, btn_facebook_success;
    private long backBtnTime = 0;
    private String success_text;
    private LoginButton btn_facebook_login;
    private LoginCallback mLoginCallback;
    private CallbackManager mCallbackManager;




    public static String getKeyHash(final Context context){ ///페이스북로그인 연동하기 위해 키해시 값 구하는 함수
        PackageManager pm= context.getPackageManager();
        try{
            PackageInfo packageInfo = pm.getPackageInfo(context.getPackageName(), PackageManager.GET_SIGNATURES);
            if(packageInfo == null)
                return null;
            for(Signature signature : packageInfo.signatures){
                try{
                    MessageDigest md=MessageDigest.getInstance("SHA");
                    md.update(signature.toByteArray());
                    return android.util.Base64.encodeToString(md.digest(), Base64.NO_WRAP);
                } catch (NoSuchAlgorithmException e){
                    e.printStackTrace();
                }
            }
        } catch (PackageManager.NameNotFoundException e){
            e.printStackTrace();
        }
        return null;
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Log.e("getKeyHash",""+getKeyHash(LoginActivity.this)); //키해시값 로그창에 출력 ==>페이스북 연동할때 필요함.

        mCallbackManager = CallbackManager.Factory.create();
        mLoginCallback = new LoginCallback();

        btn_facebook_login=(LoginButton) findViewById(R.id.btn_facebook_login);
        btn_facebook_login.setReadPermissions(Arrays.asList("public_profile", "email"));
        btn_facebook_login.registerCallback(mCallbackManager, mLoginCallback);


//        //페이스북 버튼 클릭시 수행
//        btn_facebook_login.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                Intent intent = new Intent(LoginActivity.this, LoginCallback.class);
//                startActivity(intent);
//
//            }
//        });


        et_id = findViewById(R.id.et_id);
        et_pass = findViewById(R.id.et_pass);
        btn_login = findViewById(R.id.btn_login);
        btn_register = findViewById(R.id.btn_register);
        btn_facebook_success = findViewById(R.id.btn_facebook_success);


        //회원가입 버튼 클릭시 수행
        btn_register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(LoginActivity.this, RegisterActivity.class);
                startActivity(intent);
            }
        });

        //페이스북 성공 클릭시 수행
        btn_facebook_success.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    success_text=btn_facebook_login.getText().toString();
                    if(success_text.equals("로그아웃") || success_text.equals("Log out")) {
                        Intent intent = new Intent(LoginActivity.this, ExplainActivity.class);
                        startActivity(intent);
                    }
                }

        });


        //로그인 버튼 클릭시 수행
        btn_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //저장된 값 가져옴
                final String userID = et_id.getText().toString();
                String userPass = et_pass.getText().toString();

                Response.Listener<String> responseListener = new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        try {

                            JSONObject jsonObject = new JSONObject(response);
                            boolean success = jsonObject.getBoolean("success"); //통신 성공 실패 체크
                            if(success){ //로그인 성공
                                String userID = jsonObject.getString("userID"); //getString()내의 key값 == php파일 내 키값
                                String userPass = jsonObject.getString("userPassword");

                                Toast.makeText(getApplicationContext(),"로그인에 성공하였습니다.", Toast.LENGTH_SHORT).show();
                                Intent intent = new Intent(LoginActivity.this, ExplainActivity.class); //MainActivity로 넘어감
                                startActivity(intent);
                            }else{ // 로그인 실패
                                Toast.makeText(getApplicationContext(),"로그인에 실패하였습니다.", Toast.LENGTH_SHORT).show();
                                return; //화면 넘어가지 않도록
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }//onResponse-End
                };//responseListener-익명객체-End
                LoginRequest loginRequest = new LoginRequest(userID,userPass,responseListener);
                RequestQueue queue = Volley.newRequestQueue(LoginActivity.this);
                queue.add(loginRequest);

            }//onClick-End
        });

    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data){
        mCallbackManager.onActivityResult(requestCode, resultCode, data);
        super.onActivityResult(requestCode,resultCode,data);

    }


}
