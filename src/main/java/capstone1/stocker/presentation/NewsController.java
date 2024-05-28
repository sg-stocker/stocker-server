package capstone1.stocker.presentation;

import capstone1.stocker.application.NewsService;
import capstone1.stocker.dto.NewsDto;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/tickers/{ticker}/keywords/{keywordId}")
@RequiredArgsConstructor
@Tag(name = "News Controller", description = "뉴스 컨트롤러")
public class NewsController {
    private final NewsService newsService;

    @GetMapping("/news")
    @Operation(summary = "뉴스 목록을 조회한다.", description = "키워드에 해당하는 뉴스들을 조회할 수 있다.")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "뉴스 조회 성공"),
            @ApiResponse(responseCode = "404", description = "존재하지 않는 키워드 혹은 종목코드")
    })
    public ResponseEntity<NewsDto> newsList(@PathVariable Long keywordId)
            throws Exception {
        return ResponseEntity.ok(newsService.getNews(keywordId));
    }
}
