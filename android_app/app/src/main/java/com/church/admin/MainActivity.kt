package com.church.admin

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.church.admin.api.ApiClient
import com.church.admin.ui.DashboardActivity
import com.church.admin.ui.LoginActivity
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Check if token exists
        val prefs = getSharedPreferences("church_admin", MODE_PRIVATE)
        val token = prefs.getString("auth_token", null)
        if (token != null) {
            startActivity(Intent(this, DashboardActivity::class.java))
        } else {
            startActivity(Intent(this, LoginActivity::class.java))
        }
        finish()
    }
}
