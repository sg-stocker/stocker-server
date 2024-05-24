package capstone1.stocker.dto;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
public class Oauth2Token
{
        private String access_token;
        private String token_type;
        private int expires_in;
        private String access_token_token_expired;

        private static final DateTimeFormatter DATE_TIME_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

        public boolean isExpired() {
                LocalDateTime expiryTime = LocalDateTime.parse(access_token_token_expired, DATE_TIME_FORMATTER);
                return LocalDateTime.now().isAfter(expiryTime);
        }
}
