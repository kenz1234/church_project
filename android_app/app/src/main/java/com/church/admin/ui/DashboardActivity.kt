package com.church.admin.ui

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.church.admin.R

class DashboardActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Dashboard with cards for: Prayer Requests, Queries, Events, Timings, Readings, Donations
        // Each card calls the Django REST API with auth token stored in SharedPreferences
        // Token is obtained via /api/token/ endpoint using admin credentials
    }
}
