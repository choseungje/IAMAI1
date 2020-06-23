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
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.FileProvider;

import com.gun0912.tedpermission.PermissionListener;
import com.gun0912.tedpermission.TedPermission;

import java.io.File;
import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

public class MainActivity extends AppCompatActivity {

    private Button btn_start, btn_selectPicture; //로그아웃 버튼
    private long backBtnTime = 0; //back버튼 두번 시간

    //카메라관련
    private static final int REQUEST_IMAGE_CAPTURE = 672;
    private static final int PICK_FROM_ALBUM = 673;
    private String imageFilePath;
    private Uri photoUri;
    private ImageView iv_showPicture;
    private File tempFile; //이미지 저장용





    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);




        btn_start = findViewById(R.id.btn_start);
        btn_selectPicture = findViewById(R.id.btn_selectPicture);
        iv_showPicture = findViewById(R.id.iv_showPicture);
        //로그아웃 버튼 클릭시 -> 실행버튼으로 바꿀 예정
        btn_start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
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
        }
    };

}//메인 액티비티 클래스-End

