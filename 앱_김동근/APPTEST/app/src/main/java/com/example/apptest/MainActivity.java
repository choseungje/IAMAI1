package com.example.apptest;

import android.Manifest;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.Signature;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.media.ExifInterface;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.FileProvider;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.gun0912.tedpermission.PermissionListener;
import com.gun0912.tedpermission.TedPermission;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.LoaderCallbackInterface;
import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.Mat;
import org.opencv.imgproc.Imgproc;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private Button btn_start, btn_selectPicture, btn_upload; //로그아웃 버튼
    private long backBtnTime = 0; //back버튼 두번 시간
    String imagecode ="";
    private TextView showresult;

    //카메라관련
    private static final int REQUEST_IMAGE_CAPTURE = 672;
    private static final int PICK_FROM_ALBUM = 673;
    private String imageFilePath;
    private Uri photoUri;
    private ImageView iv_showPicture;
    private File tempFile; //이미지 저장용


    //opencv
    private final static String TAG = MainActivity.class.getClass().getSimpleName();
    private boolean isOpenCvLoaded = false;
    private BaseLoaderCallback mLoaderCallback = new BaseLoaderCallback(this) {
        @Override
        public void onManagerConnected(int status) {
            switch (status) {
                case LoaderCallbackInterface.SUCCESS:
                    Log.i(TAG, "OpenCV loaded successfully");
                    break;
                default:
                    super.onManagerConnected(status);
                    break;
            }
        }
    };

    @Override
    public void onResume()
    {
        super.onResume();

        // OpenCV load
        if (!OpenCVLoader.initDebug()) {
            Log.d(TAG, "Internal OpenCV library not found. Using OpenCV Manager for initialization");
            OpenCVLoader.initAsync(OpenCVLoader.OPENCV_VERSION, this, mLoaderCallback);
        } else {
            Log.d(TAG, "OpenCV library found inside package. Using it!");
            mLoaderCallback.onManagerConnected(LoaderCallbackInterface.SUCCESS);
            isOpenCvLoaded = true;
        }
    }
    //opencv-End



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);




        btn_start = findViewById(R.id.btn_start);
        btn_selectPicture = findViewById(R.id.btn_selectPicture);
        btn_upload = findViewById(R.id.main_btn_upload);
        iv_showPicture = findViewById(R.id.iv_showPicture);
        showresult = findViewById(R.id.textView);
        //로그아웃 버튼 클릭시 -> 실행버튼으로 바꿀 예정
        btn_start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        btn_upload.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {

                Drawable dr = iv_showPicture.getDrawable();
                Bitmap imgbm = ((BitmapDrawable)dr).getBitmap();
                imgbm = Bitmap.createScaledBitmap(imgbm, 128, 128, true);
                Mat gray = new Mat();
                Utils.bitmapToMat(imgbm, gray);
                Imgproc.cvtColor(gray, gray, Imgproc.COLOR_RGB2GRAY);
                Bitmap graybitmap = Bitmap.createBitmap(gray.cols(), gray.rows(), Bitmap.Config.ARGB_8888);
                Utils.matToBitmap(gray, graybitmap);
                imagecode = gray.dump(); //픽셀값 문자열로 가져오기
                sendRequest();
            }
        });

        //사진선택 버튼 클릭시 -> 다이얼로그창
        btn_selectPicture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                AlertDialog.Builder ad_howGetPicture = new AlertDialog.Builder(MainActivity.this); //다이얼로그창 띄우기

                ad_howGetPicture.setTitle("업로드할 이미지 선택");
                //권한허용 물어봄
                TedPermission.with(getApplicationContext())
                        .setPermissionListener(permissionListener)
                        .setRationaleMessage("카메라 권한이 필요합니다.")
                        .setDeniedMessage("거부하셨습니다.")
                        .setPermissions(Manifest.permission.WRITE_EXTERNAL_STORAGE,Manifest.permission.CAMERA)
                        .check();

                //앨범선택 버튼 클릭시
                ad_howGetPicture.setNegativeButton("앨범선택", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        getPhotoFromAlbum();
                    }
                });

                //사진촬영 버튼 클릭시
                ad_howGetPicture.setPositiveButton("사진촬영", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        doTakePhotoAction();
                    }
                });

                //취소 버튼 클릭시
                ad_howGetPicture.setNeutralButton("취소", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();//창 닫기
                    }
                });

                //다이얼로그 창 보여주기
                ad_howGetPicture.show();

            }

        });

        if(AppHelper.requestQueue == null)
            AppHelper.requestQueue = Volley.newRequestQueue(getApplicationContext());
    }//onCreate-mainMethod-End


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

    //앨범에서 이미지 가져오기
    public void getPhotoFromAlbum(){
        Intent intent = new Intent(Intent.ACTION_PICK);//클릭시 앨범 열기?
        intent.setType(MediaStore.Images.Media.CONTENT_TYPE);
        startActivityForResult(intent, PICK_FROM_ALBUM);//상수설정해둔 픽프롬앨범
    }//getPhotoFromAlbum-Method_End

    // 카메라 촬영 후 이미지 가져오기
    public void doTakePhotoAction() {
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);//클릭시 카메라앱 실행
        if(intent.resolveActivity(getPackageManager()) != null){
            File photoFile = null;
            try {
                photoFile = createImageFile();
            }catch (IOException e){

            }

            if(photoFile != null){
                photoUri = FileProvider.getUriForFile(getApplicationContext(), getPackageName(),photoFile);
                intent.putExtra(MediaStore.EXTRA_OUTPUT, photoUri);
                startActivityForResult(intent, REQUEST_IMAGE_CAPTURE);//상수설정해둔 리퀘스트이미지캡쳐
            }
        }
    }//doTakePhotoAction-Method_End

    //카메라 촬영 후 이미지 갤러리에 저장
    private File createImageFile() throws IOException{
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "IAMAI_" + timeStamp + "_";
        File storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES);
        File image = File.createTempFile(imageFileName, ".jpg", storageDir);
        imageFilePath = image.getAbsolutePath();
        return image;
    }

    //앨범or카메라로 이미지 가져오기
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        //리퀘스트코드가 이미지캡쳐이면
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            Bitmap bitmap = BitmapFactory.decodeFile(imageFilePath);
            ExifInterface exif = null;

            try {
                exif = new ExifInterface(imageFilePath);
            } catch (IOException e) {
                e.printStackTrace();
            }

            int exifOrientation;
            int exifDegree;

            if (exif != null) {
                exifOrientation = exif.getAttributeInt(ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL);
                exifDegree = exifOrientationToDegrees(exifOrientation);
            } else {
                exifDegree = 0;
            }
            iv_showPicture.setImageBitmap(rotate(bitmap,exifDegree));
            //((ImageView) findViewById(R.id.iv_showPicture)).setImageBitmap(rotate(bitmap, exifDegree));

        }
        //리퀘스트코드가 픽앨범이면
        else if(requestCode == PICK_FROM_ALBUM){

            photoUri = data.getData(); //data.getData()로 선택한이미지의 Uri가져오기
            Cursor cursor = null;
            Bitmap bitmap;
            try {
                String[] imageName = {MediaStore.Images.Media.DATA};

                assert photoUri != null; //조건식이 false면 오류메시지 발생 != null : 이 부분 메시지 호출;
                cursor = getContentResolver().query(photoUri, imageName,null,null,null);

                assert cursor != null;
                int column_index = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);

                cursor.moveToFirst();
                tempFile = new File(cursor.getString(column_index));
            }finally {
                if(cursor != null)
                    cursor.close();
            }

            setImage();

        }
    }

    // 이미지 정방향
    private int exifOrientationToDegrees(int exifOrientation){
        if(exifOrientation == ExifInterface.ORIENTATION_ROTATE_90){
            return 90;
        }else if(exifOrientation == ExifInterface.ORIENTATION_ROTATE_180){
            return 180;
        }else if(exifOrientation == ExifInterface.ORIENTATION_ROTATE_270){
            return 270;
        }
        return 0;
    }

    private Bitmap rotate(Bitmap bitmap, float degree){
        Matrix matrix = new Matrix();
        matrix.postRotate(degree);
        return Bitmap.createBitmap(bitmap,0,0,bitmap.getWidth(),bitmap.getHeight(),matrix,true);
    }

    //갤러리에서 받아온 이미지 넣기
    private void setImage() {

        BitmapFactory.Options options = new BitmapFactory.Options();
        Bitmap originalBm = BitmapFactory.decodeFile(tempFile.getAbsolutePath(), options);

        iv_showPicture.setImageBitmap(originalBm);

    }


    //권한설정
    PermissionListener permissionListener = new PermissionListener() {
        @Override
        public void onPermissionGranted() {
        }

        @Override
        public void onPermissionDenied(ArrayList<String> deniedPermissions) {
            Toast.makeText(getApplicationContext(),"권한이 거부되었습니다.", Toast.LENGTH_SHORT).show();
            finish();
            startActivity(new Intent(MainActivity.this, MainActivity.class));

        }
    };

    //서버에요청
    public void sendRequest(){
        String url = "http://10.0.2.2:3000/form";

        StringRequest request = new StringRequest(
                Request.Method.POST,
                url,
                new Response.Listener<String>() { // 정상 응답
                    @Override
                    public void onResponse(String response) {
                        showresult.setText(response);
                    }
                },
                new Response.ErrorListener() { // 에러 발생
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(getApplicationContext(), error.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                }

        ){ // Post 방식으로 body에 요청 파라미터를 넣어 전달하고 싶을 경우
            // 만약 헤더를 한 줄 추가하고 싶다면 getHeaders() override
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                Map<String,String> params = new HashMap<String, String>();
                params.put("image", imagecode);

                return params;
            }
        };



        // 요청 객체를 만들었으니 이제 requestQueue 객체에 추가하면 됨.
        // Volley는 이전 결과를 캐싱하므로, 같은 결과가 있으면 그대로 보여줌
        // 하지만 아래 메소드를 false로 set하면 이전 결과가 있더라도 새로 요청해서 응답을 보여줌.
        request.setShouldCache(false);
        AppHelper.requestQueue.add(request);
    }

    //이미지 string으로 변환
    public String getStringImage(Bitmap bmp) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bmp.compress(Bitmap.CompressFormat.JPEG, 100, baos);
        byte[] imageBytes = baos.toByteArray();
        String encodedImage = Base64.encodeToString(imageBytes, Base64.DEFAULT);
        return encodedImage;

    }


}//메인 액티비티 클래스-End

