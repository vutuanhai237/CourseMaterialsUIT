using System;
using System.Windows.Forms;
using System.Media;
using System.Drawing;

namespace CountDown
{
    public partial class Form1 : Form
    {
        private int timeLeft;
        
        public Form1()
        {
            this.TopMost = true;
            InitializeComponent();
        }

        private void btnStart_Click(object sender, EventArgs e)
        {
            if (txtTimer.Text == "00:00")
            {
                MessageBox.Show("Please enter the time to start!", "Enter the Time", MessageBoxButtons.OK);
            }
            else
            {
                // Convert text to seconds as int for timer
                string[] totalSeconds = txtTimer.Text.Split(':');
                int minutes = Convert.ToInt32(totalSeconds[0]);
                int seconds = Convert.ToInt32(totalSeconds[1]);
                timeLeft = (minutes * 60) + seconds;

                // Lock Start and Clear buttons and text box
                btnStart.Enabled = false;
                btnClear.Enabled = false;
                txtTimer.ReadOnly = true;

                // Define Tick eventhandler and start timer
                //timer1.Tick += new EventHandler(Timer1_Tick);
                timer1.Start();
            }
        }

        private void btnStop_Click(object sender, EventArgs e)
        {
            timer1.Stop();
            timeLeft = 0;
            btnStart.Enabled = true;
            btnClear.Enabled = true;
            txtTimer.ReadOnly = false;
        }

        private void btnClear_Click(object sender, EventArgs e)
        {
            txtTimer.Text = "00:00";
        }

        private void Timer1_Tick(object sender, EventArgs e)
        {
            if (timeLeft > 0)
            {
                timeLeft = timeLeft - 1;
                // Display time remaining as mm:ss
                var timespan = TimeSpan.FromSeconds(timeLeft);
                txtTimer.Text = timespan.ToString(@"mm\:ss");
                txtTimer.ForeColor = Color.DodgerBlue;
            }
            else
            {
                timer1.Stop();
                SystemSounds.Exclamation.Play();
                MessageBox.Show("Thời gian đã hết, các bạn giải xong chưa?", "BHT", MessageBoxButtons.OK);
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (button1.Text.ToString() == "Hide")
            {
                this.Size = new Size(this.Size.Width, 153);
                button1.Text = "Show";
            }
            else
            {
                this.Size = new Size(this.Size.Width, 247);
                button1.Text = "Hide";
            }
        }

        private void txtTimer_TextChanged(object sender, EventArgs e)
        {

        }
    }
}