# Security Policy

## Supported Versions

We take security seriously and actively maintain security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in Riget Zoo Adventures, please report it responsibly. **Do not create a public GitHub issue for security vulnerabilities.**

### How to Report

1. **Email**: Send details to [security@riget-zoo-adventures.com] (replace with actual email)
2. **Subject Line**: Include "SECURITY VULNERABILITY" in the subject
3. **PGP**: For sensitive reports, use our PGP key (if available)

### What to Include

Please provide as much information as possible:

- **Description**: Clear description of the vulnerability
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Impact Assessment**: Your assessment of the potential impact
- **Affected Components**: Which parts of the system are affected
- **Proof of Concept**: Code or screenshots demonstrating the vulnerability (if safe to share)
- **Suggested Fix**: Any recommendations for fixing the issue (optional)

### Response Timeline

We commit to the following response times:

- **Initial Response**: Within 48 hours of receiving the report
- **Status Update**: Weekly updates until the issue is resolved
- **Fix Timeline**: Critical vulnerabilities will be addressed within 7 days, others within 30 days

## Security Best Practices

### For Users

#### Authentication & Authorization
- Use strong, unique passwords for your accounts
- Enable two-factor authentication if available
- Log out when finished, especially on shared computers
- Regularly review your account activity

#### Data Protection
- Do not share sensitive information in public areas
- Be cautious when uploading files or entering personal information
- Report suspicious activity immediately

### For Developers

#### Secure Development
- Follow OWASP security guidelines
- Validate and sanitize all user inputs
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Keep dependencies up to date

#### Django Security Features
- Always use Django's built-in CSRF protection
- Enable Django's security middleware
- Use HTTPS in production
- Set secure cookie flags
- Implement proper session management

## Common Security Considerations

### Web Application Security

#### Input Validation
```python
# Good: Proper validation
from django.core.exceptions import ValidationError

def clean_phone_number(self):
    phone = self.cleaned_data.get('phone_number')
    if phone and not phone.isdigit():
        raise ValidationError('Phone number must contain only digits')
    return phone
```

#### SQL Injection Prevention
```python
# Good: Using Django ORM (automatic protection)
users = CustomUser.objects.filter(email=user_email)

# Bad: Raw SQL (vulnerable)
# cursor.execute(f"SELECT * FROM users WHERE email = '{user_email}'")
```

#### Cross-Site Scripting (XSS) Prevention
```html
<!-- Good: Django templates auto-escape -->
<p>Welcome, {{ user.username }}!</p>

<!-- Bad: Unescaped content -->
<!-- <p>Welcome, {{ user.username|safe }}!</p> -->
```

### Infrastructure Security

#### Environment Variables
- Store sensitive configuration in environment variables
- Never commit secrets to version control
- Use `.env` files for local development
- Rotate secrets regularly

#### Database Security
- Use strong database passwords
- Limit database user permissions
- Enable database encryption at rest
- Regular security updates

#### Server Security
- Keep server operating system updated
- Use a web application firewall (WAF)
- Implement rate limiting
- Monitor for suspicious activity

## Security Checklist

### Development
- [ ] All user inputs are validated and sanitized
- [ ] SQL injection protection is implemented
- [ ] XSS protection is enabled
- [ ] CSRF protection is active
- [ ] Authentication is properly implemented
- [ ] Authorization controls are in place
- [ ] Sensitive data is encrypted
- [ ] Error messages don't leak sensitive information

### Deployment
- [ ] HTTPS is enforced
- [ ] Security headers are configured
- [ ] Debug mode is disabled in production
- [ ] Secret keys are properly secured
- [ ] Database credentials are protected
- [ ] Regular security updates are applied
- [ ] Monitoring and logging are in place
- [ ] Backup and recovery procedures are tested

## Security Tools and Resources

### Django Security
- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [Django Security Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [OWASP Django Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html)

### General Web Security
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
- [Security Headers](https://securityheaders.com/)

### Testing Tools
- [Bandit](https://bandit.readthedocs.io/) - Python security linter
- [Safety](https://pyup.io/safety/) - Dependency vulnerability scanner
- [OWASP ZAP](https://www.zaproxy.org/) - Web application security scanner

## Incident Response

### If You Suspect a Security Breach

1. **Don't Panic**: Take a systematic approach
2. **Document**: Record what you observed
3. **Isolate**: If possible, isolate the affected system
4. **Report**: Contact our security team immediately
5. **Preserve Evidence**: Don't modify affected systems
6. **Communicate**: Keep stakeholders informed

### For Maintainers

1. **Assess Impact**: Determine the scope and severity
2. **Contain**: Limit the exposure and damage
3. **Investigate**: Understand how the breach occurred
4. **Remediate**: Fix the vulnerability
5. **Monitor**: Watch for similar attacks
6. **Learn**: Update processes to prevent recurrence

## Security Updates

We regularly update our dependencies and apply security patches. Security updates will be:

- **Communicated**: Via GitHub releases and security advisories
- **Prioritized**: Critical vulnerabilities get immediate attention
- **Documented**: Changes are recorded in our changelog
- **Tested**: All updates are thoroughly tested before release

## Bug Bounty Program

Currently, we do not have a formal bug bounty program, but we greatly appreciate security researchers who help us improve our security posture. We will:

- Acknowledge your contribution in our security hall of fame
- Provide credit in our release notes
- Consider small rewards for significant discoveries (case by case)

## Contact Information

- **Security Team**: [security@riget-zoo-adventures.com] (replace with actual email)
- **General Contact**: [support@riget-zoo-adventures.com] (replace with actual email)
- **GitHub**: Open an issue for non-security related bugs

---

**Last Updated**: October 2025

Thank you for helping keep Riget Zoo Adventures secure! 🔒🦁