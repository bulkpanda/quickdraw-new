import { Component, Input, ViewChild, AfterViewInit, ElementRef} from '@angular/core';
import { fromEvent } from 'rxjs';
import { switchMap, takeUntil, pairwise } from 'rxjs/operators'
import { environment } from 'src/environments/environment';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-play',
  templateUrl: './play.component.html',
  styleUrls: ['./play.component.css']
})
export class PlayComponent implements AfterViewInit {
  @ViewChild('myCanvas') public canvas: ElementRef={} as ElementRef;
  @Input() public width=384;
  @Input() public height=384;
  private ctx: CanvasRenderingContext2D={} as CanvasRenderingContext2D;
  
  constructor(private http: HttpClient) {}
    

  

  x = "black";
  y = 3; 


   ngAfterViewInit(){
    const canvasEl: HTMLCanvasElement = this.canvas.nativeElement;
    this.ctx = <CanvasRenderingContext2D> canvasEl.getContext('2d');
    canvasEl.width=this.width;
    canvasEl.height=this.height;
    this.ctx.lineWidth =this.y;
    this.ctx.strokeStyle=this.x; 
    this.eventcapture(canvasEl);
  }

  private eventcapture(canvasEl: HTMLCanvasElement){
  
    fromEvent(canvasEl, 'mousedown')
    .pipe(
      switchMap((e)=>{
        return fromEvent(canvasEl,'mousemove')
        .pipe(
          takeUntil(fromEvent(canvasEl,'mouseup')),
          takeUntil(fromEvent(canvasEl,'mouseleave')),
          pairwise()
        )
      })
    )
    .subscribe((res: [MouseEvent,MouseEvent])=>{
      const rect=canvasEl.getBoundingClientRect();
      const prevPos={
        x:res[0].clientX - rect.left,
        y:res[0].clientY - rect.top
      };
      const currPos={
        x: res[1].clientX - rect.left,
        y: res[1].clientY - rect.top
      };
      this.draw(prevPos, currPos);
    });
    
  }

  private draw(prevPos: {x: number, y: number}, currPos: {x: number, y: number}) {
    if(!this.ctx){ return;}

    //this.pathHistory.push([prevPos, currPos]);
    this.ctx.beginPath();
    if(prevPos){
    
    this.ctx.moveTo(prevPos.x, prevPos.y);
    this.ctx.lineTo(currPos.x, currPos.y);
    this.ctx.stroke();
    }
 }
  object='';
  erase() {
        	
    this.ctx.clearRect(0, 0, this.width, this.height);
    this.object=''
  }
  
  sendimage(){
    var canvas: HTMLCanvasElement=this.canvas.nativeElement;
    var date = Date.now();
    var filename =  date + '.png';
    var image = canvas.toDataURL('image/png');
    this.http.post(environment.SERVER_URL + '/play', {filename, image},{responseType:'text'}).subscribe((res:any)=>{
      console.log(res)
      this.object="It's a " +res+"!";
      
    })
  }   
} 
