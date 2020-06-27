package com.example.apptest;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

public class RegisterActivity extends AppCompatActivity {
//회원가입 창
    private EditText et_id, et_pass, et_name, et_age;
    private Button btn_register, btn_goLogin;
    private long backBtnTime = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) { //액티비티 시작시 처음으로 실행되는 것
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        //아이디 값 찾아주기
        et_id = findViewById(R.id.et_id);
        et_pass = findViewById(R.id.et_pass);
        et_name = findViewById(R.id.et_name);
        et_age = findViewById(R.id.et_age);
        btn_goLogin = findViewById(R.id.btn_goLogin);


        //익명객체 회원가입 버튼 클릭 시 수행
        btn_register = findViewById(R.id.btn_register);
        btn_register.setOnClickListener(new View.OnClickListener() {//회원가입 버튼 클릭
            @Override
            public void onClick(View view) {
                //입력된 값 가져오기
                String userID = et_id.getText().toString();
                String userPass = et_pass.getText().toString();
                String userName = et_name.getText().toString();
                int userAge = Integer.parseInt(et_age.getText().toString());

                Response.Listener<String> responseListener = new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        try {
                            JSONObject jsonObject = new JSONObject(response);
                            boolean success = jsonObject.getBoolean("success"); //통신 성공 실패 체크
                            if(success){ //회원 가입 성공
                                Toast.makeText(getApplicationContext(),"회원 가입이 완료되었습니다.", Toast.LENGTH_SHORT).show();
                                Intent intent = new Intent(RegisterActivity.this, LoginActivity.class); //LoginActivity로 넘어감
                                startActivity(intent);
                            }else{ // 회원 가입 실패
                                Toast.makeText(getApplicationContext(),"회원 가입에 실패하였습니다.", Toast.LENGTH_SHORT).show();
                                return; //화면 넘어가지 않도록
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                };

                // volley를 이용해서 서버에 요청
                RegisterRequest registerRequest = new RegisterRequest(userID, userPass, userName, userAge, responseListener);
                RequestQueue queue = Volley.newRequestQueue(RegisterActivity.this);
                queue.add(registerRequest);

            }
        });

        //돌아가기 버튼 클릭시 수행
        btn_goLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }



    //백버튼 2번 눌러야 종료되게 설정
    @Override
    public void onBackPressed() {//뒤로가기 버튼이 눌렸을 때
        long curTime = System.currentTimeMillis();
        long gapTime = curTime - backBtnTime; //백버튼 누르는 간격 체크

        if(0 <= gapTime && gapTime <= 2000){ //2초 내에 다시 누르면 종료
            super.onBackPressed();
        }else{
            backBtnTime = curTime; //현재 시간 저장
            Toast.makeText(this,"한번 더 누르면 종료됩니다.",Toast.LENGTH_SHORT).show();
        }

    }//onBackPressed-Method-End
}
