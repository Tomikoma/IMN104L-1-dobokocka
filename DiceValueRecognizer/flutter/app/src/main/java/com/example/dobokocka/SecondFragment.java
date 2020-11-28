package com.example.dobokocka;

import android.app.Activity;
import android.content.res.AssetFileDescriptor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.ColorMatrix;
import android.os.Build;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import org.tensorflow.lite.Interpreter;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.Buffer;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.Collections;
import java.util.List;

public class SecondFragment extends Fragment {
    protected Interpreter tflite;
    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_second, container, false);
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        byte[] byteArray;
        Bitmap bmp = null;
        ByteBuffer buffer;
        float[][] modelke = new float[1][11];
        if(null != getArguments() && null != getArguments().getByteArray("image")){
            byteArray = getArguments().getByteArray("image");
            bmp = BitmapFactory.decodeByteArray(byteArray, 0, byteArray.length);
            try {
                tflite = new Interpreter(loadModelFile(this.getActivity()));
                int bytes= bmp.getByteCount();
                buffer = ByteBuffer.allocate(bytes); //Create a new buffer
                bmp.copyPixelsToBuffer(buffer); //Move the byte data to the buffer
                tflite.run(bitmapToInputArray(bmp),modelke);
                float max = 0;
                int counter = 1;
                int maxIndex = 0;
                for (float result: modelke[0]) {
                    counter++;
                    if(result > max){
                        max = result;
                        maxIndex = counter;
                    }
                }
                TextView  textView =view.findViewById(R.id.textView);
                textView.setText("A dobott összeg "+ (max*100)+ "% eséllyel: " + maxIndex+"!");
            } catch (IOException e) {
                e.printStackTrace();
            }
        } else {
            NavHostFragment.findNavController(SecondFragment.this)
                    .navigate(R.id.action_SecondFragment_to_FirstFragment);
        }
        view.findViewById(R.id.button_second).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                NavHostFragment.findNavController(SecondFragment.this)
                        .navigate(R.id.action_SecondFragment_to_FirstFragment);
            }
        });
    }
    /** Memory-map the model file in Assets. */
    private MappedByteBuffer loadModelFile(Activity activity) throws IOException {
        AssetFileDescriptor fileDescriptor = activity.getAssets().openFd("model_cnn_2.tflite");
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }

    private float[][][][] bitmapToInputArray(Bitmap bitmap1) {

        Bitmap bitmap = Bitmap.createScaledBitmap(bitmap1, 256,256, false);

        int batchNum = 0;
        float[][][][] input = new float[1][256][256][1];

        for (int x = 0; x < 256; x++) {
            for (int y = 0; y < 256; y++) {
                int pixel = bitmap.getPixel(x, y);
                // Normalize channel values to [-1.0, 1.0]. This requirement varies by
                // model. For example, some models might require values to be normalized
                // to the range [0.0, 1.0] instead.
                input[batchNum][x][y][0] = (0.299f * Color.red(pixel) + 0.587f * Color.green(pixel) + 0.114f * Color.blue(pixel))/*/ 255.0f*/;
                //input[batchNum][x][y][1] = (Color.green(pixel)) / 255.0f;
                //input[batchNum][x][y][1] = (Color.green(pixel)) / 255.0f;
                //input[batchNum][x][y][2] = (Color.blue(pixel))/ 255.0f;
            }
        }
        return input;
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    private Bitmap getBitmap(float[][][][] input) {
        int width = 256;
        int height = 256;
        Bitmap bmp = Bitmap.createBitmap(width, height, Bitmap.Config.RGB_565);

        for(int x=0; x<width; x++) {
            for(int y=0; y<height; y++) {
                float red = input[0][x][y][0];
                //int green = (int) input[0][x][y][1];
                //int blue = (int) input[0][x][y][2];

                int color = Color.rgb(red,red,red);
                bmp.setPixel(x, y, color);
            }
        }
        return bmp;
    }

}