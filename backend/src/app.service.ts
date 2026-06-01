import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHealth() {
    return {
      alive: true,
      status: 'ok',
      service: 'pdf-parser-system-api',
      checkedAt: new Date().toISOString(),
    };
  }
}
