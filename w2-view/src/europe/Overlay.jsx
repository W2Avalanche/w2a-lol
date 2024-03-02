import React from 'react';
import cx from 'classnames';
import Pick from "./Pick";

import css from './style/index.module.scss';
import Ban from "./Ban";

export default class Overlay extends React.Component {
    state = {
        currentAnimationState: css.TheAbsoluteVoid,
        openingAnimationPlayed: false
    };

    playOpeningAnimation() {
        this.setState({openingAnimationPlayed: true});
        setTimeout(() => {
            this.setState({currentAnimationState: css.AnimationHidden});
            setTimeout(() => {
                this.setState({currentAnimationState: css.AnimationTimer + ' ' + css.AnimationBansPick});
                setTimeout(() => {
                    this.setState({currentAnimationState: css.AnimationBansPick + ' ' + css.AnimationBansPickOnly});
                    setTimeout(() => {
                        this.setState({currentAnimationState: css.AnimationPigs});
                    }, 1000);
                }, 1450);
            }, 700);
        }, 500);
    }

    render() {
        const { state, config } = this.props;

        if (state.champSelectActive && !this.state.openingAnimationPlayed) {
            this.playOpeningAnimation();
        }

        if (!state.champSelectActive && this.state.openingAnimationPlayed) {
            this.setState({openingAnimationPlayed: false});
            this.setState({currentAnimationState: css.TheAbsoluteVoid});
        }

        const renderBans = (teamState) =>{
            const list =  teamState.bans.map((ban, idx) => <Ban key={`ban-${idx}`} {...ban} />);
            list.splice(3, 0, <div key="ban-spacer" className={css.Spacing} />);
            return <div className={cx(css.BansBox)}>{list}</div>;
        };

        const renderTeam = (teamName, teamConfig, teamState) => (
            <div className={cx(css.Team, teamName)}>
                <div className={cx(css.Picks)}>
                    {teamState.picks.map((pick, idx) => <Pick key={`pick-${idx}`} config={this.props.config} {...pick} />)}
                </div>
                <div className={css.BansWrapper}>
                    <div className={cx(css.Bans, {[css.WithScore]: config.scoreEnabled})}>
                        {teamName === css.TeamBlue && config.scoreEnabled && <div className={css.TeamScore}>
                            {teamConfig.score}
                        </div>}
                        {teamName === css.TeamRed && renderBans(teamState)}
                        <div className={cx(css.TeamName, {[css.WithoutCoaches]: !config.coachesEnabled})}>
                            {teamConfig.name}
                            {config.coachesEnabled && <div className={css.CoachName}>
                                Coach: {teamConfig.coach}
                            </div>}
                        </div>
                        {teamName === css.TeamBlue && renderBans(teamState)}
                        {teamName === css.TeamRed && config.scoreEnabled && <div className={css.TeamScore}>
                            {teamConfig.score}
                        </div>}
                    </div>
                </div>
            </div>
        );
            console.log(config)
        return (
            
            <div className={cx(css.Overlay, css.Europe, this.state.currentAnimationState)} style={{"--color-red": "rgb(162,8,8)", "--color-blue": "rgb(25,173,208)"}}>
                {Object.keys(state).length === 0 && <div className={cx(css.infoBox)}>Not connected to backend service!</div>}
                {Object.keys(state).length !== 0 &&
                
                    <div className={cx(css.ChampSelect)}>

                        <div className={cx(css.MiddleBox)}>
                            
                            <div className={cx(css.Logo)}>
                                <img src={!state.anyTeam ? config.logo :
                                state.blueTeam.isActive && !state.redTeam.isActive ? config.blueTeam.logo :
                                config.redTeam.logo 
                                } alt="" />

                            </div>
                            <div className={cx(css.Patch)}>
                            {!state.blueTeam.isActive && !state.redTeam.isActive ? config.tournamentName :
                                state.blueTeam.isActive && !state.redTeam.isActive ? config.blueTeam.name :
                                config.redTeam.name 
                                }                        
                            </div>
                        
                                <div className={cx(css.Timer, {
                                    [`${css.Red} ${css.Blue}`]: !state.blueTeam.isActive && !state.redTeam.isActive,
                                    [css.Blue]: state.blueTeam.isActive,
                                    [css.Red]: state.redTeam.isActive
                                })}>
                                <div className={cx(css.Background, css.Blue)} />
                                <div className={cx(css.Background, css.Red)} />

                                
                                {state.timer < 100 && <div className={cx(css.TimerChars)}>
                                    {state.timer.toString().split('').map((char, idx) => <div key={`div-${idx}`}
                                        className={cx(css.TimerChar)}></div>)}
                                </div>}

                            </div>
                        </div>
                        {renderTeam(css.TeamBlue, config.blueTeam, state.blueTeam)}
                        {renderTeam(css.TeamRed, config.redTeam, state.redTeam)}
                        {state.anyTeam ? (
                        <>
                        <div style={{
                            
                            position: 'absolute',
                            left: '80px',
                                bottom: '365px',
                                height: '10px', // Altura de la barra
                                backgroundColor: 'grey', // Color de fondo
                                width: `1760px`,
                                transformOrigin: 'center', // Establece el origen de la transformación en el centro
                                animation: 'expandFromCenter 2s linear'
                                // Ancho calculado en píxeles
                            }}>
                        </div>
                        <div style={{
                            position: 'absolute',
                            left: '960px',
                                bottom: '365px',
                                height: '10px', // Altura de la barra
                                backgroundColor: 'lightgrey', // Color de fondo
                                width: `${(state.timer / 30000) * 880}px`,
                                transition: 'width 1s linear' // Agrega esta línea
                                // Ancho calculado en píxeles
                            }}>
                        </div>
                        <div style={{
                            position: 'absolute',
                            right: '960px',
                                bottom: '365px',
                                height: '10px', // Altura de la barra
                                backgroundColor: 'lightgrey', // Color de fondo
                                width: `${(state.timer / 30000) * 880}px`,
                                transition: 'width 1s linear' // Agrega esta línea
                                // Ancho calculado en píxeles
                            }}>
                        </div>
                        </>
                        ) : null }

                    </div>
                }
            </div>
        )
    }
}
