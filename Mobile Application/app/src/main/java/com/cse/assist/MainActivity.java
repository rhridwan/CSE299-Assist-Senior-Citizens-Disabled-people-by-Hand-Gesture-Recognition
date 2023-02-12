package com.cse.assist;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class MainActivity extends AppCompatActivity {
    FirebaseDatabase database=FirebaseDatabase.getInstance();

    EditText Status, Message,Username;
    Button ViewStatus;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Username=findViewById(R.id.username);
        Status = findViewById(R.id.status);
        Message = findViewById(R.id.message);
        ViewStatus=findViewById(R.id.viewstatus);
        ViewStatus.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//Retriving Data From Firebase
                DatabaseReference Botstatus=database.getReference(String.valueOf(Username.getText()));
                Botstatus.addValueEventListener(new ValueEventListener() {
                    final String temp[]=new String[1];
                    @RequiresApi(api = Build.VERSION_CODES.O)
                    @Override
                    public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                        int i = 0;


                        for (DataSnapshot data : dataSnapshot.getChildren()) {
                            temp[i] = data.getValue().toString();
                            i++;
                        }
                        Status.setText(temp[0]);

                        try {
                            if(temp[0].equals("NORMAL")){
                                Status.setTextColor(Color.parseColor("#00ff00"));
                                Status.setText("NORMAL");
                                Message.setTextColor(Color.parseColor("#00ff00"));
                                Message.setText("Situation is normal. No need to worry about anything. Thank you for being with The Binary Knight");
                            }
                            else if (temp[0].equals("EMERGENCY")){
                                Status.setTextColor(Color.parseColor("#ff0000"));
                                Status.setText("EMERGENCY");
                                Message.setTextColor(Color.parseColor("#ff0000"));
                                Message.setText("Situation is critical. You must go to your patient right now.");
                                //PUSH NOTIFICATION
                                NotificationManager mNotificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
                                // The id of the channel.
                                String id = "my_channel_01";
                                // The user-visible name of the channel.
                                CharSequence name = getString(R.string.channel_name);
                                // The user-visible description of the channel.
                                String description = getString(R.string.channel_description);
                                int importance = NotificationManager.IMPORTANCE_LOW;
                                NotificationChannel mChannel = new NotificationChannel(id, name,importance);
                                // Configure the notification channel.
                                mChannel.setDescription(description);
                                mChannel.enableLights(true);
                                // Sets the notification light color for notifications posted to this
                                // channel, if the device supports this feature.
                                mChannel.setLightColor(Color.RED);
                                mChannel.enableVibration(true);
                                mChannel.setVibrationPattern(new long[]{100, 200, 300, 400, 500, 400, 300, 200, 400});
                                mNotificationManager.createNotificationChannel(mChannel);
                                mNotificationManager = (NotificationManager)getSystemService(Context.NOTIFICATION_SERVICE);
                                // Sets an ID for the notification, so it can be updated.
                                int notifyID = 1;
                                // The id of the channel.
                                String CHANNEL_ID = "my_channel_01";
                                // Create a notification and set the notification channel.
                                Notification notification = new Notification.Builder(MainActivity.this)
                                        .setContentTitle("Alert")
                                        .setContentText("Situation is critical.")
                                        .setSmallIcon(R.drawable.logo)
                                        .setChannelId(CHANNEL_ID)
                                        .build();
                                // Issue the notification.
                                mNotificationManager.notify(notifyID, notification);
                            }
                            else if(temp[0].equals("HELP")){
                                Status.setTextColor(Color.parseColor("#ffff00"));
                                Status.setText("HELP");
                                Message.setTextColor(Color.parseColor("#ffff00"));
                                Message.setText("No need to panic. You should go to your patient. Your help is needed");
                            }

                        }catch (Exception e){
                            Status.setTextColor(Color.parseColor("#000000"));
                            Status.setText("An unknown error occured");
                        }
                    }
                    @Override
                    public void onCancelled(@NonNull DatabaseError databaseError) {
                    }
                });
                //Retriving Data ends
            }
        });



    }
}
